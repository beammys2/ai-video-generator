import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const VideoGeneratorApp = () => {
  const [activeTab, setActiveTab] = useState('text');
  const [textPrompt, setTextPrompt] = useState('');
  const [selectedStyle, setSelectedStyle] = useState('realistic');
  const [selectedImageStyle, setSelectedImageStyle] = useState('character_animation');
  const [uploadedImage, setUploadedImage] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedVideo, setGeneratedVideo] = useState(null);
  const [videoGallery, setVideoGallery] = useState([]);
  const [styles, setStyles] = useState({});
  const [duration, setDuration] = useState(7);
  const [nsfwEnabled, setNsfwEnabled] = useState(false);
  const [showGallery, setShowGallery] = useState(false);

  useEffect(() => {
    loadStyles();
    loadVideoGallery();
  }, []);

  const loadStyles = async () => {
    try {
      const response = await axios.get(`${API}/styles`);
      setStyles(response.data);
    } catch (error) {
      console.error('Error loading styles:', error);
    }
  };

  const loadVideoGallery = async () => {
    try {
      const response = await axios.get(`${API}/videos`);
      setVideoGallery(response.data.videos);
    } catch (error) {
      console.error('Error loading gallery:', error);
    }
  };

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setUploadedImage(file);
    }
  };

  const generateTextToVideo = async () => {
    if (!textPrompt.trim()) return;
    
    setIsGenerating(true);
    try {
      const response = await axios.post(`${API}/generate-text-to-video`, {
        prompt: textPrompt,
        style: selectedStyle,
        duration: duration,
        nsfw_enabled: nsfwEnabled
      });
      
      const videoId = response.data.id;
      
      // Poll for video completion
      const checkVideo = async () => {
        try {
          const videoResponse = await axios.get(`${API}/video/${videoId}`);
          if (videoResponse.data.status === 'completed') {
            setGeneratedVideo(videoResponse.data);
            setIsGenerating(false);
            loadVideoGallery();
          } else if (videoResponse.data.status === 'failed') {
            setIsGenerating(false);
            alert('Video generation failed. Please try again.');
          } else {
            setTimeout(checkVideo, 2000);
          }
        } catch (error) {
          console.error('Error checking video status:', error);
          setIsGenerating(false);
        }
      };
      
      setTimeout(checkVideo, 1000);
    } catch (error) {
      console.error('Error generating video:', error);
      setIsGenerating(false);
    }
  };

  const generateImageToVideo = async () => {
    if (!uploadedImage) return;
    
    setIsGenerating(true);
    const formData = new FormData();
    formData.append('file', uploadedImage);
    formData.append('style', selectedImageStyle);
    formData.append('duration', duration);
    formData.append('nsfw_enabled', nsfwEnabled);
    
    try {
      const response = await axios.post(`${API}/generate-image-to-video`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      
      const videoId = response.data.id;
      
      // Poll for video completion
      const checkVideo = async () => {
        try {
          const videoResponse = await axios.get(`${API}/video/${videoId}`);
          if (videoResponse.data.status === 'completed') {
            setGeneratedVideo(videoResponse.data);
            setIsGenerating(false);
            loadVideoGallery();
          } else if (videoResponse.data.status === 'failed') {
            setIsGenerating(false);
            alert('Video generation failed. Please try again.');
          } else {
            setTimeout(checkVideo, 2000);
          }
        } catch (error) {
          console.error('Error checking video status:', error);
          setIsGenerating(false);
        }
      };
      
      setTimeout(checkVideo, 1000);
    } catch (error) {
      console.error('Error generating video:', error);
      setIsGenerating(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700 p-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
            AI Video Generator
          </h1>
          <button
            onClick={() => setShowGallery(!showGallery)}
            className="px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg transition-colors"
          >
            {showGallery ? 'Hide Gallery' : 'Show Gallery'}
          </button>
        </div>
      </header>

      <div className="max-w-6xl mx-auto p-4">
        {!showGallery ? (
          <div className="grid lg:grid-cols-2 gap-8">
            {/* Generation Panel */}
            <div className="space-y-6">
              {/* Tab Selection */}
              <div className="flex bg-gray-800 rounded-lg p-1">
                <button
                  onClick={() => setActiveTab('text')}
                  className={`flex-1 py-3 px-4 rounded-md transition-colors ${
                    activeTab === 'text'
                      ? 'bg-purple-600 text-white'
                      : 'text-gray-400 hover:text-white'
                  }`}
                >
                  Text to Video
                </button>
                <button
                  onClick={() => setActiveTab('image')}
                  className={`flex-1 py-3 px-4 rounded-md transition-colors ${
                    activeTab === 'image'
                      ? 'bg-purple-600 text-white'
                      : 'text-gray-400 hover:text-white'
                  }`}
                >
                  Image to Video
                </button>
              </div>

              {/* Text to Video Tab */}
              {activeTab === 'text' && (
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      Describe your video
                    </label>
                    <textarea
                      value={textPrompt}
                      onChange={(e) => setTextPrompt(e.target.value)}
                      placeholder="A majestic dragon flying over a medieval castle at sunset..."
                      className="w-full h-32 px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">
                      Video Style
                    </label>
                    <select
                      value={selectedStyle}
                      onChange={(e) => setSelectedStyle(e.target.value)}
                      className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-purple-500"
                    >
                      {styles.text_to_video_styles?.map((style) => (
                        <option key={style.id} value={style.id}>
                          {style.name} - {style.description}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>
              )}

              {/* Image to Video Tab */}
              {activeTab === 'image' && (
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      Upload Image
                    </label>
                    <div className="border-2 border-dashed border-gray-700 rounded-lg p-6 text-center hover:border-gray-600 transition-colors">
                      <input
                        type="file"
                        accept="image/*"
                        onChange={handleImageUpload}
                        className="hidden"
                        id="image-upload"
                      />
                      <label htmlFor="image-upload" className="cursor-pointer">
                        {uploadedImage ? (
                          <div className="space-y-2">
                            <div className="text-green-400">✓ Image uploaded</div>
                            <div className="text-sm text-gray-400">{uploadedImage.name}</div>
                          </div>
                        ) : (
                          <div className="space-y-2">
                            <div className="text-4xl">📁</div>
                            <div>Click to upload image</div>
                            <div className="text-sm text-gray-400">PNG, JPG up to 10MB</div>
                          </div>
                        )}
                      </label>
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">
                      Animation Style
                    </label>
                    <select
                      value={selectedImageStyle}
                      onChange={(e) => setSelectedImageStyle(e.target.value)}
                      className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-purple-500"
                    >
                      {styles.image_to_video_styles?.map((style) => (
                        <option key={style.id} value={style.id}>
                          {style.name} - {style.description}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>
              )}

              {/* Common Settings */}
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">
                    Duration: {duration} seconds
                  </label>
                  <input
                    type="range"
                    min="5"
                    max="10"
                    value={duration}
                    onChange={(e) => setDuration(parseInt(e.target.value))}
                    className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer slider"
                  />
                </div>

                <div className="flex items-center justify-between p-4 bg-gray-800 rounded-lg">
                  <div>
                    <div className="font-medium">NSFW Content</div>
                    <div className="text-sm text-gray-400">
                      Requires login & payment to enable
                    </div>
                  </div>
                  <div className="text-sm text-yellow-400 bg-yellow-900 px-2 py-1 rounded">
                    Premium Only
                  </div>
                </div>
              </div>

              {/* Generate Button */}
              <button
                onClick={activeTab === 'text' ? generateTextToVideo : generateImageToVideo}
                disabled={isGenerating || (activeTab === 'text' && !textPrompt.trim()) || (activeTab === 'image' && !uploadedImage)}
                className="w-full py-4 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg font-semibold text-lg transition-all"
              >
                {isGenerating ? (
                  <div className="flex items-center justify-center space-x-2">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    <span>Generating Video...</span>
                  </div>
                ) : (
                  'Generate Video'
                )}
              </button>
            </div>

            {/* Preview Panel */}
            <div className="space-y-6">
              <h2 className="text-xl font-semibold">Preview</h2>
              
              {generatedVideo ? (
                <div className="bg-gray-800 rounded-lg p-6 space-y-4">
                  <div className="aspect-video bg-gray-700 rounded-lg overflow-hidden">
                    <img
                      src={generatedVideo.thumbnail_url || generatedVideo.video_url}
                      alt="Generated video"
                      className="w-full h-full object-cover"
                    />
                  </div>
                  
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-green-400">✓ Generation Complete</span>
                      <span className="text-sm text-gray-400">
                        {generatedVideo.duration}s • {generatedVideo.style}
                      </span>
                    </div>
                    
                    {generatedVideo.prompt && (
                      <p className="text-sm text-gray-400">{generatedVideo.prompt}</p>
                    )}
                    
                    <div className="flex space-x-2 pt-2">
                      <button className="flex-1 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors">
                        Download
                      </button>
                      <button className="flex-1 py-2 bg-gray-600 hover:bg-gray-700 rounded-lg transition-colors">
                        Share
                      </button>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="bg-gray-800 rounded-lg p-12 text-center">
                  <div className="text-6xl mb-4">🎬</div>
                  <div className="text-xl mb-2">No video generated yet</div>
                  <div className="text-gray-400">
                    {activeTab === 'text' 
                      ? 'Enter a prompt and click generate to create your video'
                      : 'Upload an image and select a style to get started'
                    }
                  </div>
                </div>
              )}
            </div>
          </div>
        ) : (
          /* Gallery View */
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-semibold">Video Gallery</h2>
              <div className="text-sm text-gray-400">
                {videoGallery.length} videos generated
              </div>
            </div>
            
            {videoGallery.length > 0 ? (
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {videoGallery.map((video) => (
                  <div key={video.id} className="bg-gray-800 rounded-lg overflow-hidden">
                    <div className="aspect-video bg-gray-700">
                      <img
                        src={video.thumbnail_url || video.video_url}
                        alt="Video thumbnail"
                        className="w-full h-full object-cover"
                      />
                    </div>
                    <div className="p-4 space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-sm font-medium capitalize">
                          {video.style.replace('_', ' ')}
                        </span>
                        <span className="text-xs text-gray-400">
                          {video.duration}s
                        </span>
                      </div>
                      {video.prompt && (
                        <p className="text-sm text-gray-400 line-clamp-2">
                          {video.prompt}
                        </p>
                      )}
                      <div className="flex space-x-2 pt-2">
                        <button className="flex-1 py-1.5 text-sm bg-blue-600 hover:bg-blue-700 rounded transition-colors">
                          Download
                        </button>
                        <button className="flex-1 py-1.5 text-sm bg-gray-600 hover:bg-gray-700 rounded transition-colors">
                          Share
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-12">
                <div className="text-6xl mb-4">📱</div>
                <div className="text-xl mb-2">No videos in gallery</div>
                <div className="text-gray-400">
                  Generate your first video to see it here
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default VideoGeneratorApp;