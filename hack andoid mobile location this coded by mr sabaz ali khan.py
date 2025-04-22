from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.garden.mapview import MapView, MapMarker
from plyer import gps

Builder.load_string("""
<LocationTracker>:
    orientation: 'vertical'
    BoxLayout:
        size_hint_y: None
        height: 50
        Label:
            text: 'Live Location'
    MapView:
        id: map_view
        zoom: 15
        lat: self.center_lat
        lon: self.center_lon
        on_touch_down: self.gps_tracker.start()
        on_touch_up: self.gps_tracker.stop()
""")

class LocationTracker(BoxLayout):
    map_view = ObjectProperty()
    gps_tracker = ObjectProperty()

    def __init__(self, **kwargs):
        super(LocationTracker, self).__init__(**kwargs)
        self.gps_tracker = gps.GPS()
        self.gps_tracker.configure(on_location=self.on_location)

    def on_location(self, **kwargs):
        lat, lon = kwargs['lat'], kwargs['lon']
        self.map_view.center_lat = lat
        self.map_view.center_lon = lon
        self.map_view.add_marker(MapMarker(lat=lat, lon=lon))

class LocationTrackerApp(App):
    def build(self):
        return LocationTracker()

if __name__ == '__main__':
    LocationTrackerApp().run()