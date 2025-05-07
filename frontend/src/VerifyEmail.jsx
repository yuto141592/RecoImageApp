import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

export default function VerifyEmail() {
  const { code } = useParams();
  const navigate = useNavigate();
  const [message, setMessage] = useState('メール認証を確認しています...');

  useEffect(() => {
    fetch(`http://localhost:8000/api/verify_email/${code}/`)
      .then(res => res.json())
      .then(data => {
        if (data.message) {
          setMessage(data.message);
          setTimeout(() => navigate('/sign-in-side'), 3000); // ← ここがログイン画面への遷移先
        } else {
          setMessage(data.error || 'エラーが発生しました。');
        }
      })
      .catch(() => setMessage('通信エラーが発生しました。'));
  }, [code, navigate]);

  return (
    <div className="flex flex-col items-center justify-center h-screen text-center px-4">
      <h1 className="text-2xl font-bold mb-4">{message}</h1>
      <p className="text-gray-600">数秒後にログイン画面に移動します...</p>
    </div>
  );
}
