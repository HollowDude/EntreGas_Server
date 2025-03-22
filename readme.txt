1.Manejo de la autenticacion desde el front:
'''
// Login
const handleLogin = async () => {
    try {
        const response = await axios.post(
            'http://localhost:8000/api/auth/login/',
            { username: 'admin', password: 'password' },
            { withCredentials: true }  // Envía cookies
        );
        console.log(response.data.message);
    } catch (error) {
        console.error('Error en login:', error.response.data);
    }
};

// Logout
const handleLogout = async () => {
    try {
        const response = await axios.post(
            'http://localhost:8000/api/auth/logout/',
            {},
            { withCredentials: true }
        );
        console.log(response.data.message);
    } catch (error) {
        console.error('Error en logout:', error.response.data);
    }
};
'''