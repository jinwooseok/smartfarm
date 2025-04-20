import Image from 'next/image';

interface LoadingProps {
  size?: 'small' | 'medium' | 'large';
  className?: string;
}

export default function Loading({ size = 'medium', className = '' }: LoadingProps) {
  const sizeClasses = {
    small: 'w-6 h-6',
    medium: 'w-10 h-10',
    large: 'w-16 h-16',
  };

  return (
    <div className={`flex justify-center items-center ${className}`}>
      <div className={`relative ${sizeClasses[size]}`}>
        <Image
          src="/images/Spinner.gif"
          alt="Loading..."
          width={64}
          height={64}
          className="w-full h-full"
          priority
        />
      </div>
    </div>
  );
} 