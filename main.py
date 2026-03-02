from SpaceTrackTLEClient import SpaceTrackTLEClient

if __name__ == "__main__":
    st = SpaceTrackTLEClient("./SLTrack.ini")
    tle_obj, xlsx = st.fetch_latest_by_norad_and_save(25544)  # ISS
    print("Saved:", xlsx)