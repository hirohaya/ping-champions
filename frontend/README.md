

# Ping Champions - Frontend

This project is the frontend for the Ping Champions system, which manages events, player rankings, and match results for table tennis clubs.

## How to run locally

1. Install dependencies:
   ```sh
   npm install
   ```
2. Start the development server:
   ```sh
   npm run dev
   ```

## Project Structure
- `src/`
  - `components/`: reusable Vue components (e.g., EventCard, Breadcrumbs)
  - `views/`: main pages (e.g., EventsView, PlayersView)
  - `router/`: route configuration
  - `services/`: API integration with the backend (axios)
  - `assets/`: static files and styles

## Features
- List active events
- Create events
- Soft delete events (mark as inactive in the backend)
- Event cards with delete button and navigation to details
- Visual feedback for user actions (success/error)
- Dynamic breadcrumbs that display the event name when viewing an event or its subpages
- All user-facing text and code comments are in English for internationalization and maintainability

## Integration with Backend
- The frontend consumes REST endpoints from the FastAPI backend (see backend documentation for endpoint details).
- The default backend endpoint is `http://localhost:8000`.
- To change the API URL, edit `src/services/api.js`.

## Usage Examples
- Create event: fill out the form and click "Create Event".
- Delete event: click the trash icon on the event card.
- View details: click on the event card.

## Project Status
- [x] List, create, and delete events
- [x] Backend integration
- [x] Event cards
- [x] Dynamic breadcrumbs with event name
- [x] English standardization and improved code comments
- [ ] Player CRUD
- [ ] Match CRUD
- [ ] Ranking
- [ ] Authentication
- [ ] Visual improvements

## Contribution
Pull requests are welcome!

## License
MIT
