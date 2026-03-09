import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'epzzexqjrzqxxesqmmgi.supabase.co',
      },
    ],
  },
};

export default nextConfig;
