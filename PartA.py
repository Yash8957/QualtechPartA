import os
import json
from collections import defaultdict
import io
import time

try:
    import requests
    from ultralytics import YOLO

    # All application logic is now placed inside this 'try' block
    # to ensure it only runs if the imports are successful.
    
    # This script provides an updated solution for an Intelligent Video Analysis system.
    # It uses the ultralytics library to directly analyze images from URLs sourced
    # dynamically from the Unsplash API, without requiring a local dataset download.
    
    def fetch_image_urls_from_unsplash(query, count=5):
        """
        Fetches image URLs from the Unsplash API based on a search query.
    
        Args:
            query (str): The search term to find relevant images (e.g., 'living room').
            count (int): The number of image URLs to fetch.
    
        Returns:
            list: A list of image URLs. Returns an empty list on failure.
        """
        access_key = "YOUR_UNSPLASH_ACCESS_KEY"  # <-- REPLACE WITH YOUR ACCESS KEY
        if access_key == "YOUR_UNSPLASH_ACCESS_KEY":
            print("Error: Please replace 'YOUR_UNSPLASH_ACCESS_KEY' with your actual Unsplash API key.")
            return []
    
        url = f"https://api.unsplash.com/search/photos"
        headers = {"Authorization": f"Client-ID {access_key}"}
        params = {"query": query, "per_page": count}
    
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            image_urls = [result['urls']['regular'] for result in data['results']]
            return image_urls
        except requests.exceptions.RequestException as e:
            print(f"Error fetching images from Unsplash for query '{query}': {e}")
            return []
    
    def analyze_images_from_urls(model, image_urls, environment_type):
        """
        Analyzes images from a list of public URLs using a pre-trained model.
    
        Args:
            model (YOLO): The pre-trained YOLO model instance.
            image_urls (list): A list of URLs pointing to image files.
            environment_type (str): The type of environment being analyzed (e.g., 'home', 'shop').
    
        Returns:
            list: A list of dictionaries, each containing analysis results for one image.
        """
        if not image_urls:
            print(f"\nNo images to analyze for the {environment_type.title()} environment.")
            return []
    
        print(f"\nAnalyzing {len(image_urls)} images for the {environment_type.title()} environment...")
    
        all_image_reports = []
    
        for i, image_url in enumerate(image_urls):
            print(f"Processing image {i+1}/{len(image_urls)}: {image_url}")
            
            try:
                # Fetch the image content from the URL
                response = requests.get(image_url, timeout=10)
                response.raise_for_status() # Raise an exception for bad status codes
                
                # Use a BytesIO object to pass the image data directly to the model
                image_data = io.BytesIO(response.content)
    
                # Perform object detection on the image data
                # The 'source' argument can accept raw image data
                results = model.predict(source=image_data, conf=0.5, verbose=False)
                
            except requests.exceptions.RequestException as e:
                print(f"Error fetching image from URL {image_url}: {e}")
                continue
    
            item_counts = defaultdict(int)
            item_confidence = defaultdict(lambda: {"total": 0, "count": 0})
    
            # Process the detection results for the current image
            if results and results[0].boxes:
                for box in results[0].boxes:
                    class_id = int(box.cls)
                    confidence = float(box.conf)
                    
                    # Use the built-in class names from the YOLO model
                    item_name = model.names[class_id]
                    
                    item_counts[item_name] += 1
                    item_confidence[item_name]["total"] += confidence
                    item_confidence[item_name]["count"] += 1
            
            # Calculate average confidence for each item
            avg_confidence = {
                item: round(data["total"] / data["count"], 2)
                for item, data in item_confidence.items()
            }
            
            # Generate a structured report for the current image
            report = {
                "image_url": image_url,
                "environment_type": environment_type,
                "detected_items": []
            }
            
            for item, count in item_counts.items():
                report["detected_items"].append({
                    "item": item.title(),
                    "count": count,
                    "confidence_score": avg_confidence.get(item, 0.0)
                })
                
            all_image_reports.append(report)
            print("Analysis complete for this image.")
    
        print(f"\nAnalysis of all {environment_type} URLs is complete.")
        return all_image_reports
    
    def generate_report(report_data, output_file):
        """
        Generates a structured report in JSON format.
        
        Args:
            report_data (list): The list of report dictionaries.
            output_file (str): The path to the output JSON file.
        """
        with open(output_file, 'w') as f:
            json.dump(report_data, f, indent=4)
        print(f"Analysis report saved to {output_file}")
        
    def main():
        """
        Main function to run the item detection and counting analysis for different environments.
        """
        print("Initializing AI-powered video analysis solution.")
        
        try:
            # Load a pre-trained YOLOv8 model
            model = YOLO('yolov8n.pt')
            print("Pre-trained YOLOv8n model loaded successfully.")
    
            # --- Use Case A: Home Environment Analysis ---
            home_image_urls = fetch_image_urls_from_unsplash("living room, kitchen, bedroom", count=3)
            
            home_reports = analyze_images_from_urls(model, home_image_urls, "home")
            if home_reports:
                generate_report(home_reports, "home_analysis_report.json")
                print("\n--- Example of Home Analysis Report (First Image) ---")
                print(json.dumps(home_reports[0], indent=4))
            
            # --- Use Case B: Shop Environment Analysis ---
            shop_image_urls = fetch_image_urls_from_unsplash("supermarket, grocery store, shop", count=3)
            
            shop_reports = analyze_images_from_urls(model, shop_image_urls, "shop")
            if shop_reports:
                generate_report(shop_reports, "shop_analysis_report.json")
                print("\n--- Example of Shop Analysis Report (First Image) ---")
                print(json.dumps(shop_reports[0], indent=4))
            
        except requests.exceptions.RequestException as e:
            print(f"An unexpected error occurred during an HTTP request: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    
    if __name__ == "__main__":
        main()

except ImportError as e:
    # This block is only executed if the imports fail.
    print(f"Error: A required library was not found. Please install the necessary packages.")
    print(f"Specifically, the following import failed: {e}")
    print(f"You can install them by running 'pip install ultralytics requests'.")
    exit()
