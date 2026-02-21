/**
 * PlaceAutocomplete Utility using RapidAPI (Google Maps v2)
 */

if (typeof PlaceAutocomplete === 'undefined') {
    window.PlaceAutocomplete = class PlaceAutocomplete {
        constructor(apiKey) {
            this.apiKey = apiKey;
            this.host = 'google-map-places-new-v2.p.rapidapi.com';
            this.baseUrl = `https://${this.host}/v1/places`;
        }

        async getSuggestions(input, lat = 20.5937, lng = 78.9629) {
            if (!input || input.length < 3) return [];
            const payload = {
                input: input,
                locationBias: {
                    circle: { center: { latitude: lat, longitude: lng }, radius: 50000 }
                },
                includeQueryPredictions: true
            };
            try {
                const response = await fetch(`${this.baseUrl}:autocomplete`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Goog-FieldMask': '*',
                        'X-RapidAPI-Key': this.apiKey,
                        'X-RapidAPI-Host': this.host
                    },
                    body: JSON.stringify(payload)
                });
                const data = await response.json();
                return data.suggestions || [];
            } catch (error) {
                console.error('Autocomplete Error:', error);
                return [];
            }
        }

        async getPlaceDetails(placeId) {
            if (!placeId) return null;
            try {
                const response = await fetch(`${this.baseUrl}/${placeId}`, {
                    method: 'GET',
                    headers: {
                        'X-Goog-FieldMask': 'id,displayName,formattedAddress,location',
                        'X-RapidAPI-Key': this.apiKey,
                        'X-RapidAPI-Host': this.host
                    }
                });
                const data = await response.json();
                if (data && data.location) {
                    return {
                        lat: data.location.latitude,
                        lng: data.location.longitude,
                        address: data.formattedAddress
                    };
                }
                return null;
            } catch (error) {
                console.error('Place Details Error:', error);
                return null;
            }
        }

        async geocodeAddress(address) {
            if (!address) return null;
            try {
                const suggestions = await this.getSuggestions(address);
                if (suggestions && suggestions.length > 0) {
                    const placeId = suggestions[0].placePrediction ? suggestions[0].placePrediction.placeId : null;
                    if (placeId) return await this.getPlaceDetails(placeId);
                }
                return null;
            } catch (error) {
                console.error('Geocode Address Error:', error);
                return null;
            }
        }
    };
}

if (!window.autocompleteApiInstance) {
    window.autocompleteApiInstance = new PlaceAutocomplete('d5683c70aamsh865e63a743fd600p16939djsn74e97e3dd84f');
}

window.initAutocomplete = function (inputId, resultsId, onSelect) {
    const input = document.getElementById(inputId);
    const results = document.getElementById(resultsId);
    if (!input || !results) return;

    let debounceTimer;
    input.addEventListener('input', () => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(async () => {
            const query = input.value;
            if (query.length < 3) {
                results.innerHTML = '';
                results.style.display = 'none';
                return;
            }
            const suggestions = await window.autocompleteApiInstance.getSuggestions(query);
            if (suggestions && suggestions.length > 0) {
                results.innerHTML = suggestions.map(s => {
                    const text = s.placePrediction ? s.placePrediction.text.text : (s.queryPrediction ? s.queryPrediction.text.text : '');
                    const pId = s.placePrediction ? s.placePrediction.placeId : '';
                    return `<div class="autocomplete-item" data-place-id="${pId}">
                        <i class="fa fa-map-marker-alt me-2 text-muted"></i>
                        <span>${text}</span>
                    </div>`;
                }).join('');
                results.style.display = 'block';
                results.querySelectorAll('.autocomplete-item').forEach(item => {
                    item.addEventListener('click', async () => {
                        input.value = item.querySelector('span').textContent;
                        results.style.display = 'none';
                        const placeId = item.dataset.placeId;
                        if (placeId && onSelect) {
                            const details = await window.autocompleteApiInstance.getPlaceDetails(placeId);
                            if (details) onSelect(placeId, input.value, details.lat, details.lng);
                            else onSelect(placeId, input.value);
                        }
                    });
                });
            } else {
                results.style.display = 'none';
            }
        }, 400);
    });

    document.addEventListener('click', (e) => {
        if (!input.contains(e.target) && !results.contains(e.target)) {
            results.style.display = 'none';
        }
    });
};
