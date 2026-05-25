'use client';

import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Search, FileText, Send, CheckCircle2, PlayCircle, Loader2 } from 'lucide-react';
import axios from 'axios';

export default function Dashboard() {
  const [matches, setMatches] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [scraping, setScraping] = useState(false);
  const [applying, setApplying] = useState<string | null>(null);

  useEffect(() => {
    fetchMatches();
  }, []);

  const fetchMatches = async () => {
    try {
      setLoading(true);
      // In dev, assuming matcher service is running on 8004
      const res = await axios.get('http://localhost:8004/api/v1/matches?min_score=70');
      setMatches(res.data.matches || []);
    } catch (error) {
      console.error("Failed to fetch matches", error);
      // Fallback dummy data if service is not running
      setMatches([
        { id: "1", match_score: 92.5, job: { title: "Senior Python Developer", company: "Google" } },
        { id: "2", match_score: 85.0, job: { title: "Backend Engineer", company: "Meta" } }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleScrape = async () => {
    setScraping(true);
    try {
      await axios.post('http://localhost:8003/api/v1/scraper/jobs/search', {
        boards: ["linkedin"],
        keywords: "Software Engineer",
        location: "Remote"
      });
      alert("Scraping queued! Check back in a few minutes.");
    } catch (e) {
      console.error(e);
      alert("Failed to start scraper. Is the service running on :8003?");
    } finally {
      setScraping(false);
    }
  };

  const handleApply = async (matchId: str) => {
    setApplying(matchId);
    try {
      await axios.post('http://localhost:8006/api/v1/applications', {
        match_id: matchId,
        auto_submit: false
      });
      alert("Application process started! Form is being filled in the background.");
    } catch (e) {
      console.error(e);
      alert("Failed to start applier. Is the service running on :8006?");
    } finally {
      setApplying(null);
    }
  };

  return (
    <main className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto">
        <header className="flex justify-between items-center mb-10">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-2">
              <PlayCircle className="text-blue-600 w-8 h-8" />
              ApplyPilot Dashboard
            </h1>
            <p className="text-gray-500 mt-2">Production-grade AI Job Automation</p>
          </div>
          <div className="flex gap-4">
            <Button variant="outline" className="bg-white">
              <FileText className="w-4 h-4 mr-2" />
              Upload Resume
            </Button>
            <Button onClick={handleScrape} disabled={scraping}>
              {scraping ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : <Search className="w-4 h-4 mr-2" />}
              {scraping ? "Scraping..." : "Scrape New Jobs"}
            </Button>
          </div>
        </header>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div className="p-6 border-b border-gray-200 bg-gray-50/50">
            <h2 className="text-xl font-semibold text-gray-800">Top Matches</h2>
          </div>
          
          <div className="divide-y divide-gray-200">
            {loading ? (
              <div className="p-12 text-center text-gray-500 flex justify-center items-center">
                <Loader2 className="w-6 h-6 animate-spin mr-2" /> Loading matches...
              </div>
            ) : matches.length === 0 ? (
              <div className="p-12 text-center text-gray-500">No matches found. Try scraping some jobs!</div>
            ) : (
              matches.map((match) => (
                <div key={match.id} className="p-6 hover:bg-blue-50/30 transition-colors flex items-center justify-between">
                  <div className="flex items-start gap-4">
                    <div className="w-16 h-16 rounded-full bg-blue-100 flex items-center justify-center text-blue-700 font-bold text-lg border-4 border-white shadow-sm">
                      {Math.round(match.match_score)}%
                    </div>
                    <div>
                      <h3 className="text-lg font-bold text-gray-900">{match.job.title}</h3>
                      <p className="text-gray-600 font-medium">{match.job.company}</p>
                      <p className="text-sm text-gray-500 mt-1 flex items-center gap-1">
                        <CheckCircle2 className="w-4 h-4 text-green-500" />
                        Skills match your parsed resume
                      </p>
                    </div>
                  </div>
                  <div className="flex flex-col gap-2">
                    <Button 
                      onClick={() => handleApply(match.id)} 
                      disabled={applying === match.id}
                      className="w-32"
                    >
                      {applying === match.id ? (
                        <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                      ) : (
                        <Send className="w-4 h-4 mr-2" />
                      )}
                      Auto-Apply
                    </Button>
                    <Button variant="outline" size="sm" className="w-32 text-xs">
                      Tailor PDF
                    </Button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
