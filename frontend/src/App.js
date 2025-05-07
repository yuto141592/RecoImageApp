import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SignUp from './sign-up/SignUp';
import SignInSide from './sign-in-side/SignInSide'; // ログイン画面
import VerifyEmail from './VerifyEmail'; // メール認証画面（新規作成）
import Blog from './blog/Blog';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<SignUp />} />
        <Route path="/sign-in-side" element={<SignInSide />} />
        <Route path="/verify_email/:code" element={<VerifyEmail />} />
        <Route path="/blog" element={<Blog />} />
      </Routes>
    </Router>
  );
}

export default App;
