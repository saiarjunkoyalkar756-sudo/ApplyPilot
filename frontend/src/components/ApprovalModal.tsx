'use client';

import React from 'react';
import { Button } from '@/components/ui/button';
import { Check, X, ExternalLink, Image as ImageIcon, Loader2 } from 'lucide-react';

interface ApprovalModalProps {
  application: any;
  onApprove: (id: string) => void;
  onCancel: (id: string) => void;
  isOpen: boolean;
}

export default function ApprovalModal({ application, onApprove, onCancel, isOpen }: ApprovalModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-md z-[60] flex items-center justify-center p-4">
      <div className="bg-white rounded-3xl w-full max-w-4xl max-h-[90vh] overflow-hidden flex flex-col shadow-2xl">
        <header className="p-6 border-b flex justify-between items-center bg-gray-50">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Final Review Required</h2>
            <p className="text-gray-500">The robot has filled your application. Please verify before submission.</p>
          </div>
          <Button variant="ghost" onClick={() => onCancel(application.id)}>
            <X className="w-6 h-6" />
          </Button>
        </header>

        <div className="flex-1 overflow-y-auto p-8 grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="space-y-6">
            <section>
              <h3 className="text-sm font-semibold text-blue-600 uppercase tracking-wider mb-3">Job Details</h3>
              <div className="bg-blue-50/50 p-4 rounded-xl border border-blue-100">
                <p className="font-bold text-gray-900">{application.job_title}</p>
                <p className="text-gray-700">{application.company}</p>
                <a href={application.job_url} target="_blank" className="text-blue-600 text-sm flex items-center gap-1 mt-2 hover:underline">
                  View Original Posting <ExternalLink className="w-3 h-3" />
                </a>
              </div>
            </section>

            <section>
              <h3 className="text-sm font-semibold text-green-600 uppercase tracking-wider mb-3">AI Tailoring Notes</h3>
              <div className="bg-green-50/50 p-4 rounded-xl border border-green-100 text-sm text-gray-700 leading-relaxed">
                "We've highlighted your 3 years of Python experience and emphasized the Intelligent Insurance Platform project to match this role's focus on scalable backend systems."
              </div>
            </section>

            <div className="pt-4 space-y-3">
              <Button onClick={() => onApprove(application.id)} className="w-full h-14 text-lg bg-green-600 hover:bg-green-700 shadow-lg shadow-green-100">
                <Check className="w-5 h-5 mr-2" />
                Approve & Submit Application
              </Button>
              <Button variant="outline" onClick={() => onCancel(application.id)} className="w-full h-12 text-gray-600 border-gray-200">
                Discard Draft
              </Button>
            </div>
          </div>

          <div className="flex flex-col h-full">
            <h3 className="text-sm font-semibold text-purple-600 uppercase tracking-wider mb-3 flex items-center gap-2">
              <ImageIcon className="w-4 h-4" />
              Proof of Filling (Screenshot)
            </h3>
            <div className="flex-1 bg-gray-100 rounded-2xl border-2 border-dashed border-gray-300 flex items-center justify-center overflow-hidden relative group">
              {application.screenshot ? (
                <img src={application.screenshot} alt="Form proof" className="w-full h-full object-contain" />
              ) : (
                <div className="text-center p-8">
                  <Loader2 className="w-8 h-8 text-gray-400 animate-spin mx-auto mb-2" />
                  <p className="text-gray-400 text-sm">Waiting for screenshot...</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
