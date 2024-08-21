Momentscape
===========

A social media platform built with Django Rest Framework (DRF), React, Tailwind CSS, and SQLite. Momentscape allows users to share photos, videos, and text content, react to posts, comment on posts, and update their profiles.

Project Links:
--------------
- Preview: https://moment-scape.vercel.app/
- Client-Side Code: https://github.com/Rocky3698/MomentScape
- Server-Side Code: https://github.com/Rocky3698/MomentScape_REST_API

Key Features:
-------------
- **User Authentication:** Secure user authentication and authorization.
- **Content Sharing:** Users can share photos, videos, and text content.
- **Reactions and Comments:** Users can react to and comment on posts.
- **Profile Management:** Users can update their profiles with new information.

Technologies Used:
------------------
- **Backend:** Django Rest Framework (DRF)
- **Frontend:** React, Tailwind CSS
- **Database:** SQLite

Setup Instructions:
-------------------
1. **Clone the repositories:**
   - `git clone https://github.com/Rocky3698/MomentScape`
   - `git clone https://github.com/Rocky3698/MomentScape_REST_API`

2. **Backend Setup:**
   - Navigate to the `MomentScape_REST_API` directory.
   - Create a virtual environment: `python -m venv env`
   - Activate the virtual environment:
     - On Windows: `env\Scripts\activate`
     - On MacOS/Linux: `source env/bin/activate`
   - Install dependencies: `pip install -r requirements.txt`
   - Apply migrations: `python manage.py migrate`
   - Start the server: `python manage.py runserver`

3. **Frontend Setup:**
   - Navigate to the `MomentScape` directory.
   - Install dependencies: `npm install`
   - Start the development server: `npm start`

4. **Access the application:**
   - Open your browser and navigate to `http://localhost:3000` for the frontend.
   - The backend API will be running on `http://localhost:8000`.

Contributing:
-------------
We welcome contributions to Momentscape! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes.
4. Push the branch to your forked repository.
5. Open a pull request to the main repository.

Contact:
--------
For any questions or issues, please reach out to Rocky Chowdhury at [rocky20809@gmail.com](mailto:rocky20809@gmail.com).

License:
--------
This project is licensed under the MIT License. See the LICENSE file for more details.
