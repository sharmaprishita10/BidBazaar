# Commerce

Commerce is a web-based project designed to create an eBay-like e-commerce auction site where users can post auction listings, place bids, comment on listings, and manage a personalized "Watchlist".

### Description

This project involves developing an online auction platform that enables users to interact through listings. Users can create auctions, place bids, add comments, and categorize their items. It supports authentication and personalized user experiences, including a watchlist for tracking specific listings.

### Getting Started

1. Run the following commands:
```bash
python manage.py makemigrations auctions
python manage.py migrate
python manage.py runserver
```
2. Visit http://127.0.0.1:8000/ in your web browser to use the e-commerce auction site.

### Specification

#### Create Listing
- Users can visit a page to create a new listing.
- They can specify a title, description, and starting bid for the listing.
- Optionally, users can provide a URL for an image and a category (e.g., Fashion, Toys, Electronics, Home, etc.).

#### Active Listings Page
- For each active listing, the page shows:
  - Title
  - Description
  - Current price
  - Photo (if one exists for the listing)

#### Listing Page
- Users can view all details about the specific listing, including the current price.
- If the user is signed in:
  - They can add the item to their “Watchlist” or remove it.
  - They can bid on the item. 
  - If the user created the listing, they can close the auction, declaring the highest bidder as the winner.
- Users can add comments to the listing page. 

#### Watchlist
- Signed-in users can visit a "Watchlist" page to view all listings they’ve added.

#### Categories
- A page displays all listing categories.
- Clicking a category name shows all active listings in that category.

#### Additional Feature

- **Error Handling**: Ensures bids meet minimum criteria.

### CSS and Design

The design is simple and intuitive, allowing for seamless navigation and interaction.

### About

This project was developed to demonstrate proficiency in Django web development, focusing on dynamic content generation, user authentication, and database management.

### Video Demo

You can view a video showcasing the project on [YouTube](https://www.youtube.com/watch?v=C4cciMTVjgQ).
