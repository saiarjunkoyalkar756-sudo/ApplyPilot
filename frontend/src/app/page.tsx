import React from 'react';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm">
        <h1 className="text-4xl font-bold mb-8 text-center text-blue-600">🚀 Job Copilot Production Platform</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
            <h2 className="text-xl font-semibold mb-4">1. Auth & Profiles</h2>
            <p className="text-gray-600 text-sm">Sign in to sync your preferences and application pipeline.</p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
            <h2 className="text-xl font-semibold mb-4">2. Upload Resume</h2>
            <p className="text-gray-600 text-sm">Use the AI Parser service to digitize your experiences.</p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
            <h2 className="text-xl font-semibold mb-4">3. Scrape Jobs</h2>
            <p className="text-gray-600 text-sm">Fetch latest opportunities from Indeed, LinkedIn, and more.</p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
            <h2 className="text-xl font-semibold mb-4">4. Match Scores</h2>
            <p className="text-gray-600 text-sm">View vector-matched jobs that fit your profile perfectly.</p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
            <h2 className="text-xl font-semibold mb-4">5. Tailor & Build</h2>
            <p className="text-gray-600 text-sm">Generate optimized PDF resumes for each specific job.</p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
            <h2 className="text-xl font-semibold mb-4">6. Auto-Apply</h2>
            <p className="text-gray-600 text-sm">Let Playwright fill out applications on autopilot.</p>
          </div>
        </div>
      </div>
    </main>
  );
}
