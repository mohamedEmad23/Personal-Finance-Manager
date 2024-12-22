import React, { useState } from 'react';
import { signup } from '../../services/authService';
import { useNavigate } from 'react-router-dom';

const Register = () => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleSignup = async (e) => {
        e.preventDefault();
        try {
            const userData = await signup({ name, email, password }); // Assuming `userData` includes `userId`
            console.log('User signed up:', userData);

            // Redirect to dashboard with userId
            navigate('/dashboard', { state: { userId: userData.id } });
        } catch (error) {
            console.error('Signup error:', error);
            alert('Registration failed');
        }
    };

    return (
        <div className="login">
            <h2>Register</h2>
            <form onSubmit={handleSignup}>
                <input
                    type="text"
                    placeholder="Username"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button type="submit">Register</button>
            </form>
        </div>
    );
};

export default Register;
