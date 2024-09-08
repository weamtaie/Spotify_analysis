import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load the dataset
final_data = pd.read_csv('updated_spotify_data.csv')

st.title("Spotify Dashboard 🎵📊")

# Sidebar for User Input
st.sidebar.header("Filter Options")

selected_artist = st.sidebar.selectbox('Select Artist', ['All'] + list(final_data['artist_name'].unique()))
selected_playlist = st.sidebar.selectbox('Select Playlist', ['All'] + list(final_data['name'].unique()))
year_range = st.sidebar.slider('Select Release Year Range', 
                               int(final_data['release_year'].min()), 
                               int(final_data['release_year'].max()), 
                               (2011, 2017))

# Filter the data based on user inputs
filtered_data = final_data.copy()

if selected_artist != 'All':
    filtered_data = filtered_data[filtered_data['artist_name'] == selected_artist]

if selected_playlist != 'All':
    filtered_data = filtered_data[filtered_data['name'] == selected_playlist]

filtered_data = filtered_data[(filtered_data['release_year'] >= year_range[0]) & 
                              (filtered_data['release_year'] <= year_range[1])]

# Check if filtered data is empty
if filtered_data.empty:
    st.write("No data available for the selected filters.")
else:
    # Prepare data for different visualizations based on filtered data

    # Distribution of tracks by release year
    release_year_distribution = filtered_data['release_year'].value_counts().reset_index()
    release_year_distribution.columns = ['release_year', 'track_count']

    # Top 10 artists based on the number of tracks
    artist_popularity = filtered_data['artist_name'].value_counts().reset_index().head(10)
    artist_popularity.columns = ['artist_name', 'track_count']

   
    # Top 10 most listened to artists
    top_artists = filtered_data['artist_name'].value_counts().nlargest(10).reset_index()
    top_artists.columns = ['artist_name', 'count']

    # Top 10 most listened to songs
    top_songs = filtered_data['track_name'].value_counts().nlargest(10).reset_index()
    top_songs.columns = ['track_name', 'count']

    # Top 10 playlists by number of followers
    top_playlists_by_followers = filtered_data.groupby('name')['num_followers'].max().reset_index()
    top_playlists_by_followers = top_playlists_by_followers.sort_values('num_followers', ascending=False).head(10)

    # Group by release year and track name, then count occurrences
    most_popular_track_each_year = filtered_data.groupby(['release_year', 'track_name']).size().reset_index(name='count')
    most_popular_track_each_year = most_popular_track_each_year.loc[most_popular_track_each_year.groupby('release_year')['count'].idxmax()]

    # Group by release year and platlist name, then count occurrences
    most_popular_playlist_each_year = filtered_data.groupby(['release_year', 'name']).size().reset_index(name='count')
    most_popular_playlist_each_year = most_popular_playlist_each_year.loc[most_popular_playlist_each_year.groupby('release_year')['count'].idxmax()]

    #   Find the most popular playlist for each year based on number of followers
    most_popular_playlist_each_year_followers = filtered_data.loc[filtered_data.groupby('release_year')['num_followers'].idxmax()][['release_year', 'name', 'num_followers']]

    # Total number of followers per year
    followers_per_year = filtered_data.groupby('release_year')['num_followers'].sum().reset_index()
    followers_per_year.columns = ['release_year', 'total_followers']

    # Visualizations

 
    # Visualization for Total Followers per Year as a Pie Chart
    st.subheader('Spotify Activity by Year (Based on Number of Followers)')
    fig = px.pie(followers_per_year, 
                 names='release_year', 
                 values='total_followers',
                 title='Most Active Years on Spotify Based on Number of Followers')
    fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
    st.plotly_chart(fig)
    st.subheader('Distribution of Tracks by Release Year')
    fig = px.bar(release_year_distribution, x='release_year', y='track_count', labels={'release_year': 'Release Year', 'track_count': 'Number of Tracks'}, color='track_count')
    fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
    st.plotly_chart(fig)

# Display Most Popular Track for Each Year
    st.subheader('Most Popular Track Each Year')
    fig = px.bar(most_popular_track_each_year, x='release_year', y='count', color='track_name',
                 labels={'release_year': 'Release Year', 'count': 'Number of Plays', 'track_name': 'Track Name'},
                 title='Most Popular Track Each Year')
    fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
    st.plotly_chart(fig)


# Display Most Popular playlist for Each Year
    st.subheader('Most Popular Playlist Each Year')
    fig = px.bar(most_popular_playlist_each_year, x='release_year', y='count', color='name',
                 labels={'release_year': 'Release Year', 'count': 'Number of Plays', 'name': 'Playlist Name'},
                 title='Most Popular Playlist Each Year')
    fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
    st.plotly_chart(fig)

    # Display Most Popular Playlist Each Year Based on Number of Followers
    st.subheader('Most Popular Playlist Each Year Based on Number of Followers')
    fig = px.bar(most_popular_playlist_each_year_followers, x='release_year', y='num_followers', color='name',
                 labels={'release_year': 'Release Year', 'num_followers': 'Number of Followers', 'name': 'Playlist Name'},
                 title='Most Popular Playlist Each Year Based on Number of Followers')
    fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
    st.plotly_chart(fig)

    # Visualization: Top 10 Most Listened to Artists
    st.subheader('Top 10 Most Listened to Artists')
    fig, ax = plt.subplots()
    sns.barplot(x='count', y='artist_name', data=top_artists, palette='viridis', ax=ax)
    ax.set_title('Top 10 Most Listened to Artists')
    ax.set_xlabel('Count', color='white')  # X-axis label color
    ax.set_ylabel('Artist Name', color='white')  # Y-axis label color
    ax.tick_params(axis='both', colors='white')  # Tick color
    fig.patch.set_alpha(0.0)  # Set figure background to be transparent
    ax.patch.set_alpha(0.0)   # Set axes background to be transparent
    st.pyplot(fig)

    # Visualization: Top 10 Most Listened to Songs
    st.subheader('Top 10 Most Listened to Songs')
    fig, ax = plt.subplots()
    sns.barplot(x='count', y='track_name', data=top_songs, palette='viridis', ax=ax)
    ax.set_title('Top 10 Most Listened to Songs')
    ax.set_xlabel('Count', color='white')  # X-axis label color
    ax.set_ylabel('Artist Name', color='white')  # Y-axis label color
    ax.tick_params(axis='both', colors='white')  # Tick color
    fig.patch.set_alpha(0.0)  # Set figure background to be transparent
    ax.patch.set_alpha(0.0)   # Set axes background to be transparent
    st.pyplot(fig)

    # Visualization: Top 10 Playlists by Number of Followers
    st.subheader('Top 10 Playlists by Number of Followers')
    fig, ax = plt.subplots()
    sns.barplot(x='num_followers', y='name', data=top_playlists_by_followers, palette='viridis', ax=ax)
    ax.set_title('Top 10 Playlists by Number of Followers')
    ax.set_xlabel('Count', color='white')  # X-axis label color
    ax.set_ylabel('Artist Name', color='white')  # Y-axis label color
    ax.tick_params(axis='both', colors='white')  # Tick color
    fig.patch.set_alpha(0.0)  # Set figure background to be transparent
    ax.patch.set_alpha(0.0)   # Set axes background to be transparent
    st.pyplot(fig)




# ////////////////////////////////////////////////////////////////////////////////
# # User selections for filtering data
# selected_artist = st.sidebar.selectbox('Select Artist', final_data['artist_name'].unique())
# selected_playlist = st.sidebar.selectbox('Select Playlist', final_data['name'].unique())
# year_range = st.sidebar.slider('Select Release Year Range', int(final_data['release_year'].min()), int(final_data['release_year'].max()), (2011, 2017))


# # Prepare data for different visualizations
# release_year_distribution = final_data['release_year'].value_counts().reset_index()
# release_year_distribution.columns = ['release_year', 'track_count']

# artist_popularity = final_data['artist_name'].value_counts().reset_index().head(10)
# artist_popularity.columns = ['artist_name', 'track_count']

# top_artists = final_data['artist_name'].value_counts().nlargest(10).reset_index()
# top_artists.columns = ['artist_name', 'count']

# top_songs = final_data['track_name'].value_counts().nlargest(10).reset_index()
# top_songs.columns = ['track_name', 'count']

# top_playlists_by_followers = final_data.groupby('name')['num_followers'].max().reset_index()
# top_playlists_by_followers = top_playlists_by_followers.sort_values('num_followers', ascending=False).head(10)

# # Add other necessary preprocessing steps here...


# # Filter the data based on user inputs
# filtered_data = final_data[(final_data['artist_name'] == selected_artist) & (final_data['name'] == selected_playlist)]
# filtered_data = filtered_data[(filtered_data['release_year'] >= year_range[0]) & (final_data['release_year'] <= year_range[1])]

# # Bar chart using Plotly
# fig1 = px.bar(filtered_data, x='release_year', y='track_duration_m', color='artist_name',
#               title='Track Duration by Release Year')
# st.plotly_chart(fig1)

# # Boxplot for track duration distribution by playlist
# plt.figure(figsize=(7, 3))
# sns.boxplot(x='name', y='track_duration_m', data=filtered_data, palette='viridis')
# plt.title('Track Duration Distribution by Playlist')
# st.pyplot(plt)
 
# # Prepare data for different visualizations
# release_year_distribution = filtered_data['release_year'].value_counts().reset_index()
# release_year_distribution.columns = ['release_year', 'track_count']

# artist_popularity = final_data['artist_name'].value_counts().reset_index().head(10)
# artist_popularity.columns = ['artist_name', 'track_count']

# top_artists = final_data['artist_name'].value_counts().nlargest(10).reset_index()
# top_artists.columns = ['artist_name', 'count']

# top_songs = final_data['track_name'].value_counts().nlargest(10).reset_index()
# top_songs.columns = ['track_name', 'count']

# top_playlists_by_followers = final_data.groupby('name')['num_followers'].max().reset_index()
# top_playlists_by_followers = top_playlists_by_followers.sort_values('num_followers', ascending=False).head(10)

# # 1. Bar Chart: Distribution of Tracks by Release Year

# st.subheader('Distribution of Tracks by Release Year')
# fig = px.bar(release_year_distribution, x='release_year', y='track_count',
#              title='Distribution of Tracks by Release Year',
#              labels={'release_year': 'Release Year', 'track_count': 'Number of Tracks'},
#              color='track_count')
# st.plotly_chart(fig)

# # 2. Bar Chart: Top 10 Popular Artists Based on Number of Tracks

# st.subheader('Top 10 Popular Artists Based on Number of Tracks')
# fig, ax = plt.subplots()
# sns.barplot( filtered_data ,x='artist_name', y='track_count', data=artist_popularity, ax=ax, palette='viridis')
# ax.set_title('Top 10 Popular Artists')
# plt.xticks(rotation=45)
# st.pyplot(fig)

# # 3. Pie Chart: Distribution of Tracks by Release Year
# st.subheader('Pie Chart: Distribution of Tracks by Release Year')
# fig, ax = plt.subplots()
# ax.pie(release_year_distribution['track_count'], labels=release_year_distribution['release_year'].astype(str), autopct='%1.1f%%', colors=['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FFB3E6'], startangle=140)
# plt.title('Distribution of Tracks by Release Year')
# st.pyplot(fig)

# # Repeat this for other visualizations...

# # Insights Section
# st.write("## Insights")
# st.write("""
# - **Most Popular Genres**: Display the top genres in the city based on listening habits.
# - **Top Artists and Songs**: Provide the most listened to artists and songs based on the filtered data.
# - **Trends Analysis**: Show trends in listening habits over the selected time range.
# """)