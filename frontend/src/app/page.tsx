'use client';

import { useState, useEffect } from 'react';
import Loading from '@/components/Loading';

export default function Home() {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // 페이지 로딩 시 2초 후에 로딩 상태 해제
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 2000);

    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      {isLoading ? (
        <Loading size="large" />
      ) : (
        <h1>Hello World</h1>
      )}
    </div>
  );
}
