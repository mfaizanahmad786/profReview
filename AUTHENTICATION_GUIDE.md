# Frontend Authentication Implementation Guide

## Overview
Authentication has been successfully integrated into the frontend React application, connecting with the existing FastAPI backend authentication system.

## What Was Added

### 1. **AuthContext** (`src/context/AuthContext.jsx`)
- Global authentication state management using React Context API
- Functions: `login()`, `signup()`, `logout()`, `isAuthenticated`
- Automatic token storage in localStorage
- Automatic user session restoration on app load
- Centralized error handling

### 2. **Login Page** (`src/pages/Login.jsx`)
- Beautiful, modern login form with email and password
- Password visibility toggle
- Error message display
- Automatic redirect to home page after successful login
- Link to signup page

### 3. **Signup Page** (`src/pages/Signup.jsx`)
- Registration form with email and password
- Password strength requirements with visual indicators:
  - At least 8 characters
  - One uppercase letter
  - One lowercase letter
  - One number
- Password confirmation field
- Automatic login after successful signup
- Link to login page

### 4. **ProtectedRoute Component** (`src/components/ProtectedRoute.jsx`)
- Higher-order component to protect routes that require authentication
- Automatically redirects to login if user is not authenticated
- Shows loading state while checking authentication

### 5. **ReviewModal Component** (`src/components/ReviewModal.jsx`)
- Modal form for writing professor reviews
- Requires authentication (redirects to login if not logged in)
- Features:
  - Star rating for overall rating (1-5)
  - Star rating for difficulty level (1-5)
  - Yes/No for "Would take again"
  - Course taken (optional)
  - Grade received dropdown (optional)
  - Review comment textarea
- Automatic data refresh after review submission

### 6. **Updated Components**

#### **App.jsx**
- Wrapped with `AuthProvider` for global authentication state
- Added routes for `/login` and `/signup`

#### **Navbar.jsx**
- Shows different UI based on authentication state:
  - **Not logged in**: Login and Sign Up buttons
  - **Logged in**: User email display and Logout button
- Logout functionality with one click

#### **ProfessorProfile.jsx**
- Integrated ReviewModal for writing reviews
- "Write a Review" button opens the modal
- Automatic page refresh after review submission

## How It Works

### Authentication Flow

1. **Login/Signup**:
   - User enters credentials
   - Frontend sends request to backend API
   - Backend returns JWT token
   - Token is stored in localStorage
   - User data is fetched and stored in AuthContext
   - User is redirected to home page

2. **Authenticated Requests**:
   - API interceptor automatically adds JWT token to all requests
   - Token is included in `Authorization: Bearer <token>` header
   - Backend validates token and processes request

3. **Session Persistence**:
   - On app load, AuthContext checks for stored token
   - If token exists, fetches current user data
   - User remains logged in across browser sessions

4. **Logout**:
   - Removes token from localStorage
   - Clears user data from AuthContext
   - Updates UI to show login/signup options

### Protected Actions

- **Writing Reviews**: Requires authentication
  - Clicking "Write a Review" opens modal if logged in
  - If not logged in, redirects to login page
  - After login, can write review

## API Endpoints Used

All endpoints are in `src/services/api.js`:

- `POST /auth/login` - Login with email and password
- `POST /auth/signup` - Register new user
- `GET /auth/me` - Get current user data
- `POST /reviews` - Create a new review (requires auth token)

## Usage Examples

### Using Authentication in Components

```jsx
import { useAuth } from '../context/AuthContext';

function MyComponent() {
  const { isAuthenticated, user, login, logout } = useAuth();

  if (isAuthenticated) {
    return <div>Welcome, {user.email}!</div>;
  }

  return <button onClick={() => navigate('/login')}>Login</button>;
}
```

### Protecting Routes

```jsx
import ProtectedRoute from './components/ProtectedRoute';

<Route 
  path="/protected" 
  element={
    <ProtectedRoute>
      <ProtectedComponent />
    </ProtectedRoute>
  } 
/>
```

## Testing the Implementation

1. **Start the backend server**:
   ```bash
   cd server
   source venv/bin/activate
   uvicorn app.main:app --reload
   ```

2. **Start the frontend**:
   ```bash
   cd client
   npm run dev
   ```

3. **Test Signup**:
   - Navigate to http://localhost:5173/signup
   - Enter email and password (must meet requirements)
   - Click "Create Account"
   - Should auto-login and redirect to home

4. **Test Login**:
   - Navigate to http://localhost:5173/login
   - Enter your credentials
   - Click "Sign In"
   - Should redirect to home with user info in navbar

5. **Test Review Creation**:
   - Go to any professor profile
   - Click "Write a Review"
   - If logged in, modal opens
   - Fill out the form and submit
   - Review should appear in the list

6. **Test Logout**:
   - Click the "Logout" button in navbar
   - Should see Login/Sign Up buttons again
   - Token removed from localStorage

## Security Features

- ✅ JWT token-based authentication
- ✅ Password hashing on backend (bcrypt)
- ✅ Token automatically included in API requests
- ✅ Protected routes require authentication
- ✅ Secure token storage in localStorage
- ✅ Automatic token validation on each request
- ✅ Password strength requirements

## Future Enhancements (Optional)

- Email verification
- Password reset functionality
- Remember me option
- Social login (Google, GitHub, etc.)
- User profile page
- Edit/delete own reviews
- Admin panel for managing users/reviews

## Troubleshooting

### Token not being sent with requests
- Check that token is in localStorage: `localStorage.getItem('token')`
- Check API interceptor in `src/services/api.js`

### Login returns 401 error
- Verify backend is running
- Check that email and password are correct
- Check backend logs for errors

### Reviews not requiring authentication
- Ensure ReviewModal checks `isAuthenticated`
- Verify token is being sent with POST /reviews request
- Check backend route has authentication dependency

## Files Modified/Created

**Created:**
- `src/context/AuthContext.jsx`
- `src/pages/Login.jsx`
- `src/pages/Signup.jsx`
- `src/components/ProtectedRoute.jsx`
- `src/components/ReviewModal.jsx`

**Modified:**
- `src/App.jsx`
- `src/components/Navbar.jsx`
- `src/pages/ProfessorProfile.jsx`
- `src/components/DepartmentAvatar.jsx` (unified colors)

**Existing (already had auth endpoints):**
- `src/services/api.js`
