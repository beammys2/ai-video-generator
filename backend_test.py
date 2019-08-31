import requests
import unittest
import time
import os
import json
from io import BytesIO
from PIL import Image

# Get the backend URL from the frontend .env file
with open('/app/frontend/.env', 'r') as f:
    for line in f:
        if line.startswith('REACT_APP_BACKEND_URL='):
            BACKEND_URL = line.strip().split('=')[1].strip('"\'')
            break

API_URL = f"{BACKEND_URL}/api"

class AIVideoGeneratorAPITest(unittest.TestCase):
    """Test suite for the AI Video Generator API"""

    def setUp(self):
        """Setup before each test"""
        self.api_url = API_URL
        # Create a test image for image-to-video tests
        self.test_image = self._create_test_image()
    
    def _create_test_image(self):
        """Create a simple test image"""
        img = Image.new('RGB', (100, 100), color='red')
        img_io = BytesIO()
        img.save(img_io, 'JPEG')
        img_io.seek(0)
        return img_io
    
    def test_01_styles_endpoint(self):
        """Test the styles endpoint returns correct data"""
        print("\n🔍 Testing /api/styles endpoint...")
        
        response = requests.get(f"{self.api_url}/styles")
        
        self.assertEqual(response.status_code, 200, "Styles endpoint should return 200 OK")
        data = response.json()
        
        # Verify the structure of the response
        self.assertIn('text_to_video_styles', data, "Response should contain text_to_video_styles")
        self.assertIn('image_to_video_styles', data, "Response should contain image_to_video_styles")
        
        # Verify text-to-video styles
        text_styles = data['text_to_video_styles']
        self.assertTrue(len(text_styles) > 0, "Should have at least one text-to-video style")
        self.assertIn('id', text_styles[0], "Style should have an id")
        self.assertIn('name', text_styles[0], "Style should have a name")
        self.assertIn('description', text_styles[0], "Style should have a description")
        
        # Verify image-to-video styles
        image_styles = data['image_to_video_styles']
        self.assertTrue(len(image_styles) > 0, "Should have at least one image-to-video style")
        
        print("✅ Styles endpoint test passed")
        return text_styles[0]['id'], image_styles[0]['id']
    
    def test_02_text_to_video_generation(self):
        """Test the text-to-video generation endpoint"""
        print("\n🔍 Testing /api/generate-text-to-video endpoint...")
        
        # Get a valid style from the styles endpoint
        text_style, _ = self.test_01_styles_endpoint()
        
        # Test data
        data = {
            "prompt": "A dragon flying over a castle",
            "style": text_style,
            "duration": 7,
            "nsfw_enabled": False
        }
        
        # Make the request
        response = requests.post(f"{self.api_url}/generate-text-to-video", json=data)
        
        # Verify response
        self.assertEqual(response.status_code, 200, "Text-to-video endpoint should return 200 OK")
        result = response.json()
        
        # Verify response structure
        self.assertIn('id', result, "Response should contain video id")
        self.assertEqual(result['prompt'], data['prompt'], "Prompt should match")
        self.assertEqual(result['style'], data['style'], "Style should match")
        self.assertEqual(result['duration'], data['duration'], "Duration should match")
        self.assertEqual(result['status'], "generating", "Initial status should be 'generating'")
        
        # Store the video ID for later tests
        video_id = result['id']
        print(f"✅ Text-to-video generation initiated with ID: {video_id}")
        
        # Wait for video generation to complete (should take about 3 seconds)
        print("⏳ Waiting for video generation to complete...")
        time.sleep(4)  # Wait a bit longer than the 3 seconds simulation
        
        # Check the video status
        response = requests.get(f"{self.api_url}/video/{video_id}")
        self.assertEqual(response.status_code, 200, "Video status endpoint should return 200 OK")
        
        result = response.json()
        self.assertEqual(result['status'], "completed", "Video status should be 'completed'")
        self.assertIsNotNone(result['video_url'], "Video URL should be present")
        self.assertIsNotNone(result['thumbnail_url'], "Thumbnail URL should be present")
        
        print("✅ Text-to-video generation test passed")
        return video_id
    
    def test_03_image_to_video_generation(self):
        """Test the image-to-video generation endpoint"""
        print("\n🔍 Testing /api/generate-image-to-video endpoint...")
        
        # Get a valid style from the styles endpoint
        _, image_style = self.test_01_styles_endpoint()
        
        # Prepare the multipart form data
        files = {
            'file': ('test_image.jpg', self.test_image, 'image/jpeg')
        }
        data = {
            'style': image_style,
            'duration': 7,
            'nsfw_enabled': 'false'
        }
        
        # Make the request
        response = requests.post(f"{self.api_url}/generate-image-to-video", files=files, data=data)
        
        # Verify response
        self.assertEqual(response.status_code, 200, "Image-to-video endpoint should return 200 OK")
        result = response.json()
        
        # Verify response structure
        self.assertIn('id', result, "Response should contain video id")
        self.assertEqual(result['style'], image_style, "Style should match")
        self.assertEqual(result['duration'], 7, "Duration should match")
        self.assertEqual(result['status'], "generating", "Initial status should be 'generating'")
        
        # Store the video ID for later tests
        video_id = result['id']
        print(f"✅ Image-to-video generation initiated with ID: {video_id}")
        
        # Wait for video generation to complete (should take about 3 seconds)
        print("⏳ Waiting for video generation to complete...")
        time.sleep(4)  # Wait a bit longer than the 3 seconds simulation
        
        # Check the video status
        response = requests.get(f"{self.api_url}/video/{video_id}")
        self.assertEqual(response.status_code, 200, "Video status endpoint should return 200 OK")
        
        result = response.json()
        self.assertEqual(result['status'], "completed", "Video status should be 'completed'")
        self.assertIsNotNone(result['video_url'], "Video URL should be present")
        self.assertIsNotNone(result['thumbnail_url'], "Thumbnail URL should be present")
        
        print("✅ Image-to-video generation test passed")
        return video_id
    
    def test_04_get_video_by_id(self):
        """Test getting a video by ID"""
        print("\n🔍 Testing /api/video/{id} endpoint...")
        
        # Generate a video first
        video_id = self.test_02_text_to_video_generation()
        
        # Get the video
        response = requests.get(f"{self.api_url}/video/{video_id}")
        
        # Verify response
        self.assertEqual(response.status_code, 200, "Get video endpoint should return 200 OK")
        result = response.json()
        
        # Verify response structure
        self.assertEqual(result['id'], video_id, "Video ID should match")
        self.assertEqual(result['status'], "completed", "Video status should be 'completed'")
        
        print("✅ Get video by ID test passed")
    
    def test_05_get_videos_gallery(self):
        """Test getting the videos gallery"""
        print("\n🔍 Testing /api/videos endpoint...")
        
        # Make sure we have at least one video in the gallery
        self.test_02_text_to_video_generation()
        
        # Get the gallery
        response = requests.get(f"{self.api_url}/videos")
        
        # Verify response
        self.assertEqual(response.status_code, 200, "Videos gallery endpoint should return 200 OK")
        result = response.json()
        
        # Verify response structure
        self.assertIn('videos', result, "Response should contain videos array")
        self.assertIn('total_count', result, "Response should contain total_count")
        self.assertTrue(len(result['videos']) > 0, "Gallery should have at least one video")
        self.assertTrue(result['total_count'] > 0, "Total count should be greater than 0")
        
        # Verify video structure in gallery
        video = result['videos'][0]
        self.assertIn('id', video, "Video should have an id")
        self.assertIn('style', video, "Video should have a style")
        self.assertIn('status', video, "Video should have a status")
        self.assertIn('video_url', video, "Video should have a video_url")
        
        print("✅ Videos gallery test passed")

if __name__ == '__main__':
    print("🧪 Starting AI Video Generator API Tests")
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    print("🎉 All API tests completed")