# This Python script will generate a zip file structure for the separate login system
# with all backend and frontend files prefilled with starter code.

import os
import zipfile

# Define folder structure and starter files
project_name = 'login-system'
structure = {
    'backend': {
        'server.js': 'const express = require(\'express\');\nconst mongoose = require(\'mongoose\');\nconst cors = require(\'cors\');\nrequire(\'dotenv\').config();\n\nconst authUserRoutes = require(\'./routes/authUser\');\nconst authStaffRoutes = require(\'./routes/authStaff\');\n\nconst app = express();\napp.use(cors());\napp.use(express.json());\n\napp.use(\'/api/user\', authUserRoutes);
app.use(\'/api/staff\', authStaffRoutes);
\nconst PORT = process.env.PORT || 5000;
\nmongoose.connect(process.env.MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => app.listen(PORT, () => console.log(`Server running on port ${PORT}`)))
  .catch(err => console.error(err));',
        'routes': {
            'authUser.js': "const express = require('express');\nconst router = express.Router();\nconst User = require('../models/User');\nconst bcrypt = require('bcrypt');\nconst jwt = require('jsonwebtoken');\n\n// User signup\nrouter.post('/signup', async (req, res) => { const { name, email, password } = req.body; try { let user = await User.findOne({ email }); if(user) return res.status(400).json({ msg:'User exists'}); user = new User({ name, email, password, role:'user'}); await user.save(); const token = jwt.sign({id:user._id, role:user.role}, process.env.JWT_SECRET,{expiresIn:'1h'}); res.json({ token, user:{ id:user._id, name, email, role:user.role } }); } catch(err){res.status(500).send('Server error');} });\n\n// User login\nrouter.post('/login', async (req, res)=>{ const { email, password } = req.body; try{ const user = await User.findOne({ email, role:'user'}); if(!user) return res.status(400).json({ msg:'Invalid credentials'}); const isMatch = await bcrypt.compare(password, user.password); if(!isMatch) return res.status(400).json({ msg:'Invalid credentials'}); const token = jwt.sign({id:user._id, role:user.role}, process.env.JWT_SECRET,{expiresIn:'1h'}); res.json({ token, user:{ id:user._id, name:user.name, email:user.email, role:user.role } }); } catch(err){res.status(500).send('Server error');} });\n\nmodule.exports = router;",
            'authStaff.js': "const express = require('express');\nconst router = express.Router();\nconst User = require('../models/User');\nconst bcrypt = require('bcrypt');\nconst jwt = require('jsonwebtoken');\n\n// Staff signup\nrouter.post('/signup', async (req, res) => { const { name, email, password } = req.body; try { let user = await User.findOne({ email }); if(user) return res.status(400).json({ msg:'Staff exists'}); user = new User({ name, email, password, role:'staff'}); await user.save(); const token = jwt.sign({id:user._id, role:user.role}, process.env.JWT_SECRET,{expiresIn:'1h'}); res.json({ token, user:{ id:user._id, name, email, role:user.role } }); } catch(err){res.status(500).send('Server error');} });\n\n// Staff login\nrouter.post('/login', async (req, res)=>{ const { email, password } = req.body; try{ const user = await User.findOne({ email, role:'staff'}); if(!user) return res.status(400).json({ msg:'Invalid credentials'}); const isMatch = await bcrypt.compare(password, user.password); if(!isMatch) return res.status(400).json({ msg:'Invalid credentials'}); const token = jwt.sign({id:user._id, role:user.role}, process.env.JWT_SECRET,{expiresIn:'1h'}); res.json({ token, user:{ id:user._id, name:user.name, email:user.email, role:user.role } }); } catch(err){res.status(500).send('Server error');} });\n\nmodule.exports = router;"
        },
        'models': {
            'User.js': "const mongoose = require('mongoose');\nconst bcrypt = require('bcrypt');\nconst UserSchema = new mongoose.Schema({ name:{type:String, required:true}, email:{type:String, required:true, unique:true}, password:{type:String, required:true}, role:{type:String, required:true} });\nUserSchema.pre('save', async function(next){ if(!this.isModified('password')) return next(); const salt = await bcrypt.genSalt(10); this.password = await bcrypt.hash(this.password, salt); next(); });\nmodule.exports = mongoose.model('User', UserSchema);"
        },
        'config': {
            'db.js': "const mongoose = require('mongoose'); require('dotenv').config(); const connectDB = async()=>{ try{ await mongoose.connect(process.env.MONGO_URI,{ useNewUrlParser:true, useUnifiedTopology:true }); console.log('MongoDB connected'); }catch(err){ console.error(err.message); process.exit(1); } }; module.exports=connectDB;"
        }
    },
    'frontend': {
        'public': {
            'index.html': '<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"UTF-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><title>Login System</title></head><body><div id=\"root\"></div></body></html>'
        },
        'src': {
            'index.js': "import React from 'react'; import ReactDOM from 'react-dom/client'; import App from './App'; ReactDOM.createRoot(document.getElementById('root')).render(<React.StrictMode><App /></React.StrictMode>);",
            'App.jsx': "import React from 'react'; import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'; import UserLogin from './components/UserLogin'; import UserSignup from './components/UserSignup'; import StaffLogin from './components/StaffLogin'; import StaffSignup from './components/StaffSignup'; import UserDashboard from './components/UserDashboard'; import StaffDashboard from './components/StaffDashboard'; function App(){ return (<Router><Routes><Route path='/user/login' element={<UserLogin/>}/><Route path='/user/signup' element={<UserSignup/>}/><Route path='/staff/login' element={<StaffLogin/>}/><Route path='/staff/signup' element={<StaffSignup/>}/><Route path='/user/dashboard' element={<UserDashboard/>}/><Route path='/staff/dashboard' element={<StaffDashboard/>}/></Routes></Router>); } export default App;",
            'components': {
                'UserLogin.jsx': "import React, { useState } from 'react'; import axios from 'axios'; import { useNavigate } from 'react-router-dom'; function UserLogin(){ const [email,setEmail]=useState(''); const [password,setPassword]=useState(''); const navigate=useNavigate(); const handleSubmit=async(e)=>{ e.preventDefault(); try{ const res=await axios.post('http://localhost:5000/api/user/login',{email,password}); localStorage.setItem('token',res.data.token); navigate('/user/dashboard'); }catch(err){alert(err.response.data.msg);}}; return(<form onSubmit={handleSubmit}><h2>User Login</h2><input type='email' placeholder='Email' value={email} onChange={e=>setEmail(e.target.value)}/><input type='password' placeholder='Password' value={password} onChange={e=>setPassword(e.target.value)}/><button type='submit'>Login</button></form>);} export default UserLogin;",
                'UserSignup.jsx': "import React,{useState} from 'react'; import axios from 'axios'; import { useNavigate } from 'react-router-dom'; function UserSignup(){ const [name,setName]=useState(''); const [email,setEmail]=useState(''); const [password,setPassword]=useState(''); const navigate=useNavigate(); const handleSubmit=async(e)=>{ e.preventDefault(); try{ const res=await axios.post('http://localhost:5000/api/user/signup',{name,email,password}); localStorage.setItem('token',res.data.token); navigate('/user/dashboard'); }catch(err){alert(err.response.data.msg);}}; return(<form onSubmit={handleSubmit}><h2>User Signup</h2><input placeholder='Name' value={name} onChange={e=>setName(e.target.value)}/><input placeholder='Email' value={email} onChange={e=>setEmail(e.target.value)}/><input placeholder='Password' type='password' value={password} onChange={e=>setPassword(e.target.value)}/><button type='submit'>Signup</button></form>);} export default UserSignup;",
                'StaffLogin.jsx': "import React,{useState} from 'react'; import axios from 'axios'; import { useNavigate } from 'react-router-dom'; function StaffLogin(){ const [email,setEmail]=useState(''); const [password,setPassword]=useState(''); const navigate=useNavigate(); const handleSubmit=async(e)=>{ e.preventDefault(); try{ const res=await axios.post('http://localhost:5000/api/staff/login',{email,password}); localStorage.setItem('token',res.data.token); navigate('/staff/dashboard'); }catch(err){alert(err.response.data.msg);}}; return(<form onSubmit={handleSubmit}><h2>Staff Login</h2><input placeholder='Email' value={email} onChange={e=>setEmail(e.target.value)}/><input type='password' placeholder='Password' value={password} onChange={e=>setPassword(e.target.value)}/><button type='submit'>Login</button></form>);} export default StaffLogin;",
                'StaffSignup.jsx': "import React,{useState} from 'react'; import axios from 'axios'; import { useNavigate } from 'react-router-dom'; function StaffSignup(){ const [name,setName]=useState(''); const [email,setEmail]=useState(''); const [password,setPassword]=useState(''); const navigate=useNavigate(); const handleSubmit=async(e)=>{ e.preventDefault(); try{ const res=await axios.post('http://localhost:5000/api/staff/signup',{name,email,password}); localStorage.setItem('token',res.data.token); navigate('/staff/dashboard'); }catch(err){alert(err.response.data.msg);}}; return(<form onSubmit={handleSubmit}><h2>Staff Signup</h2><input placeholder='Name' value={name} onChange={e=>setName(e.target.value)}/><input placeholder='Email' value={email} onChange={e=>setEmail(e.target.value)}/><input type='password' placeholder='Password' value={password} onChange={e=>setPassword(e.target.value)}/><button type='submit'>Signup</button></form>);} export default StaffSignup;",
                'UserDashboard.jsx': "import React from 'react'; function UserDashboard(){ return(<div><h2>User Dashboard</h2></div>);} export default UserDashboard;",
                'StaffDashboard.jsx': "import React from 'react'; function StaffDashboard(){ return(<div><h2>Staff Dashboard</h2></div>);} export default StaffDashboard;"
            }
        }
    },
    '.env':'MONGO_URI=your_mongodb_connection_string\nJWT_SECRET=your_jwt_secret',
    'package.json':'{
  "name": "login-backend",
  "version": "1.0.0",
  "main": "server.js",
  "scripts": {"start": "node backend/server.js"},
  "dependencies": {"express":"^4.18.2","mongoose":"^7.5.0","cors":"^2.8.5","dotenv":"^16.3.1","bcrypt":"^5.2.1","jsonwebtoken":"^9.2.2"}
}',
    'README.md':'Login system with separate user and staff authentication.'
}

# Function to create zip

def create_zip(path, structure, zipf, parent=''):
    for name, content in structure.items():
        full_path = os.path.join(parent, name)
        if isinstance(content, dict):
            create_zip(path, content, zipf, full_path)
        else:
            zipf.writestr(full_path, content)

# Create the zip
zip_filename = 'login-system.zip'
with zipfile.ZipFile(zip_filename, 'w') as zipf:
    create_zip(project_name, structure, zipf)

print(f'{zip_filename} created successfully.')