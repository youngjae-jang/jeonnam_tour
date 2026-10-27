"""Display the selected attraction and nearby restaurants on a Folium map."""
import html
import folium
import streamlit as st
from streamlit_folium import st_folium


def render_restaurant_map(tour, restaurants, widget_key):
    center = [float(tour["latitude"]), float(tour["longitude"])]
    fmap = folium.Map(location=center, zoom_start=13, control_scale=True)
    folium.Marker(center, tooltip=str(tour["title"]), icon=folium.Icon(color="blue", icon="info-sign")).add_to(fmap)
    for place in restaurants:
        if place.latitude is None or place.longitude is None:
            continue
        folium.Marker(
            [place.latitude, place.longitude],
            tooltip=place.name,
            popup=folium.Popup(html.escape(place.name), max_width=240),
            icon=folium.Icon(color="green", icon="cutlery", prefix="fa"),
        ).add_to(fmap)
    st_folium(fmap, key=widget_key, height=360, use_container_width=True, returned_objects=[])
