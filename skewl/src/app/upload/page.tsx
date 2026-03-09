import { UploadForm } from '@/components/UploadForm';

export default function UploadPage() {
  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Upload a Video</h1>
      <UploadForm />
    </div>
  );
}
