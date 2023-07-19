export default {
    name: "Map",
    data() {
        return {
            center: [37, 7749, -122, 4194]
        }
    },
    methods: {
        setupLeafletMap: function() {
            const mapDiv = L.map("map-container").setView(this.center, 13);
            L.tileLayer(
                "https://stamen-tiles-{s}.a.ssl.fastly.net/terrain-background/{z}/{x}/{y}{r}.{ext}", {
                    attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                    maxZoom: 18,
                    id: "mapbox/streets-v11",
                }
            ).addTo(mapDiv);
        },
    },
    mounted() {
        this.setupLeafletMap();
    },
};
