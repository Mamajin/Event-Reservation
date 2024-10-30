import React, { useEffect } from 'react';
import { Loader } from '@googlemaps/js-api-loader';
import { FiMapPin } from "react-icons/fi";

const GOOGLE_MAPS_API_KEY = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;

function Map({ formData, setFormData, setError }) {
  useEffect(() => {
    const loader = new Loader({
      apiKey: GOOGLE_MAPS_API_KEY,
      version: 'weekly',
      libraries: ['places']
    });

    loader.load().then(() => {
      const mapElement = document.getElementById('map');
      const mapInstance = new google.maps.Map(mapElement, {
        center: { lat: 13.848186926276574, lng: 100.57228692526716 },
        zoom: 8,
        styles: [
          {
            featureType: 'all',
            elementType: 'geometry',
            stylers: [{ color: '#242f3e' }]
          },
          {
            featureType: 'water',
            elementType: 'geometry',
            stylers: [{ color: '#17263c' }]
          }
        ]
      });

      const input = document.getElementById('address-input');
      const autocompleteInstance = new google.maps.places.Autocomplete(input);

      const markerInstance = new google.maps.Marker({
        map: mapInstance,
        position: mapInstance.getCenter(),
        title: "Event Location",
        draggable: true,
        icon: {
          path: google.maps.SymbolPath.CIRCLE,
          scale: 10,
          fillColor: '#F59E0B',
          fillOpacity: 1,
          strokeColor: '#ffffff',
          strokeWeight: 2,
        }
      });

      autocompleteInstance.addListener('place_changed', () => {
        const place = autocompleteInstance.getPlace();
        if (place.geometry && place.geometry.location) {
          mapInstance.setCenter(place.geometry.location);
          mapInstance.setZoom(15);
          markerInstance.position = place.geometry.location;
          setFormData(prev => ({
            ...prev,
            address: place.formatted_address || '',
            latitude: place.geometry.location.lat(),
            longitude: place.geometry.location.lng(),
          }));
        }
      });

      markerInstance.addListener('dragend', () => {
        const position = markerInstance.getPosition();
        if (position) {
          setFormData(prev => ({
            ...prev,
            latitude: position.lat(),
            longitude: position.lng(),
          }));

          const geocoder = new google.maps.Geocoder();
          geocoder.geocode({ location: position }, (results, status) => {
            if (status === 'OK' && results?.[0]) {
              setFormData(prev => ({
                ...prev,
                address: results[0].formatted_address,
              }));
              input.value = results[0].formatted_address;
            }
          });
        }
      });
    }).catch(err => {
      setError('Failed to load Google Maps. Please try again later.');
      console.error('Google Maps loading error:', err);
    });
  }, [setFormData, setError]);

  return (
    <div className="space-y-4">
      <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <FiMapPin className="h-5 w-5 text-gray-400" />
        </div>
        <input
          id="address-input"
          type="text"
          name="address"
          value={formData.address}
          onChange={(e) => setFormData(prev => ({ ...prev, address: e.target.value }))}
          className="pl-10 input bg-gray-100 input-bordered w-full"
          placeholder="Enter event location"
          required
        />
      </div>
      <div className="h-64 rounded-lg overflow-hidden border border-gray-300">
        <div id="map" className="w-full h-full"></div>
      </div>
    </div>
  );
}

export default Map;
  