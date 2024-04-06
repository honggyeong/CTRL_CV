import folium
import streamlit as st
import matplotlib.pyplot as plt
from streamlit_folium import st_folium


st.title('도움받기')

with st.container():
    # Starting variables
    center = [35.95, 128.25]
    zoom = 6
    use_time = False
    colormap = plt.cm.YlOrRd
    padding_geo_factor = 1 / 111111
    interpolation_algo_dict = {
        'idw': 'Inverse Distance Weighting (IDW)',
        'tin': 'Triangular Irregular Network (TIN)'
    }
    is_extended_graph = True

    # State variables
    if 'center' not in st.session_state:
        st.session_state.center = center

    if 'source' not in st.session_state:
        st.session_state.source = center

    if 'zoom' not in st.session_state:
        st.session_state.zoom = zoom

    if "cost_type" not in st.session_state:
        st.session_state.cost_type = 'distance'

    # Map
    m = folium.Map(location=center, zoom_start=zoom)

    with st.form("map_form"):

        # Map Controls
        st.subheader('위치 선택')
        st.caption('지도를 움직여 위치를 바꿔주세요')

        # Create the map
        with st.container():

            # When the user pans the map ...
            map_state_change = st_folium(
                m,
                key="new",
                height=300,
                width='100%',
                returned_objects=['center', 'zoom'],
            )

            st.write('⌖')

            if 'center' in map_state_change:
                st.session_state.center = [map_state_change['center']['lat'], map_state_change['center']['lng']]

            if 'zoom' in map_state_change:
                st.session_state.zoom = map_state_change['zoom']

        with st.container():
            col1, col2 = st.columns([2, 1])

            with col1:
                dec = 10
                st.write(round(st.session_state.center[0], dec), ', ', round(st.session_state.center[1], dec))

            with col2:
                submitted = st.form_submit_button("Set location")
                if submitted:
                    st.session_state.source = st.session_state.center
                    st.title('입력되었습니다')