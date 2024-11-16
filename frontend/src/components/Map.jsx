import React, { useEffect } from 'react';
import { Loader } from '@googlemaps/js-api-loader';


const GOOGLE_MAPS_API_KEY = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;

function Map({ form, setError }) {
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
      mapInstance.setZoom(15);
      const input = document.getElementById('address-input');
      const autocompleteInstance = new google.maps.places.Autocomplete(input);
      const markerInstance = new google.maps.Marker({
        map: mapInstance,
        position: mapInstance.getCenter(),
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
          markerInstance.setPosition(place.geometry.location);

          form.setValue('address', place.formatted_address || '');
          form.setValue('latitude', place.geometry.location.lat());
          form.setValue('longitude', place.geometry.location.lng());
        }
      });

      markerInstance.addListener('dragend', () => {
        const position = markerInstance.getPosition();
        if (position) {
          form.setValue('latitude', position.lat());
          form.setValue('longitude', position.lng());

          const geocoder = new google.maps.Geocoder();
          geocoder.geocode({ location: position }, (results, status) => {
            if (status === 'OK' && results?.[0]) {
              form.setValue('address', results[0].formatted_address);
              input.value = results[0].formatted_address;
            }
          });
        }
      });
    }).catch(err => {
      setError('Failed to load Google Maps. Please try again later.');
      console.error('Google Maps loading error:', err);
    });
  }, [form, setError]);

  return (
    <div className="h-64 rounded-lg overflow-hidden border border-gray-300">
      <div id="map" className="w-full h-full"></div>
    </div>
  );
}

export default Map;
