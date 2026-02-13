import { Link } from "wouter";
import { Button } from "@/components/ui/button";
import {
  Shield,
  Eye,
  Database,
  Lock,
  AlertTriangle,
  ArrowRight,
} from "lucide-react";

export default function AboutPage() {
  return (
    <div>
      {/* Hero */}
      <section className="bg-[#0C2E4C] text-white py-16">
        <div className="container max-w-4xl mx-auto px-4 text-center">
          <h1 className="text-3xl md:text-4xl font-bold mb-4">About Yesveri</h1>
          <p className="text-[#A3CCDC] text-lg max-w-2xl mx-auto">
            Election claim verification powered by official data.
            We show alignment — you decide the truth.
          </p>
        </div>
      </section>

      {/* Mission */}
      <section className="py-16">
        <div className="container max-w-3xl mx-auto px-4">
          <h2 className="text-3xl font-bold mb-6 text-center">Our Mission</h2>
          <div className="space-y-5 text-muted-foreground leading-relaxed text-center max-w-2xl mx-auto text-lg">
            <p>
              Yesveri helps people verify election claims against official sources
              during a period when AI-generated misinformation is cheap and trust is
              fragile. We don't decide truth — we make official records accessible
              and show how claims align with what the Electoral Commission actually
              announced.
            </p>
            <p>
              Our goal is to make disagreement visible: show what a claim says, what
              the official record says, and let people draw their own conclusions.
            </p>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-16 bg-muted/30">
        <div className="container max-w-4xl mx-auto px-4">
          <h2 className="text-3xl font-bold mb-10 text-center">How It Works</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white rounded-lg border shadow-sm p-8">
              <div className="flex items-center gap-3 mb-4">
                <div className="h-12 w-12 rounded-lg bg-[#0C2E4C] flex items-center justify-center flex-shrink-0">
                  <Database className="h-6 w-6 text-white" />
                </div>
                <h3 className="text-lg font-semibold">1. Data Collection</h3>
              </div>
              <p className="text-base text-muted-foreground leading-relaxed">
                We collect and store official Electoral Commission results with
                source URLs and retrieval timestamps. Every data point is
                traceable to its official origin.
              </p>
            </div>
            <div className="bg-white rounded-lg border shadow-sm p-8">
              <div className="flex items-center gap-3 mb-4">
                <div className="h-12 w-12 rounded-lg bg-[#1C7393] flex items-center justify-center flex-shrink-0">
                  <Eye className="h-6 w-6 text-white" />
                </div>
                <h3 className="text-lg font-semibold">2. Entity Extraction</h3>
              </div>
              <p className="text-base text-muted-foreground leading-relaxed">
                When you submit a claim (text or image), we extract candidate
                names, vote counts, percentages, and constituencies using NLP
                and OCR.
              </p>
            </div>
            <div className="bg-white rounded-lg border shadow-sm p-8">
              <div className="flex items-center gap-3 mb-4">
                <div className="h-12 w-12 rounded-lg bg-[#1F9CB4] flex items-center justify-center flex-shrink-0">
                  <Shield className="h-6 w-6 text-white" />
                </div>
                <h3 className="text-lg font-semibold">3. Deterministic Matching</h3>
              </div>
              <p className="text-base text-muted-foreground leading-relaxed">
                Extracted fields are compared against official records using
                deterministic rules — no scoring or confidence percentages.
                A number either matches or it doesn't.
              </p>
            </div>
            <div className="bg-white rounded-lg border shadow-sm p-8">
              <div className="flex items-center gap-3 mb-4">
                <div className="h-12 w-12 rounded-lg bg-[#0C2E4C] flex items-center justify-center flex-shrink-0">
                  <Eye className="h-6 w-6 text-white" />
                </div>
                <h3 className="text-lg font-semibold">4. Transparent Results</h3>
              </div>
              <p className="text-base text-muted-foreground leading-relaxed">
                Results show what we extracted, what the official record says,
                which fields match, and which differ. You decide what it means.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Privacy */}
      <section className="py-16">
        <div className="container max-w-3xl mx-auto px-4">
          <div className="text-center mb-8">
            <div className="h-12 w-12 rounded-lg bg-[#0C2E4C] flex items-center justify-center mx-auto mb-4">
              <Lock className="h-6 w-6 text-white" />
            </div>
            <h2 className="text-3xl font-bold">Privacy</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-white rounded-lg border shadow-sm p-6">
              <p className="text-base text-muted-foreground leading-relaxed">
                Uploaded images are processed for text extraction and immediately
                discarded — never stored.
              </p>
            </div>
            <div className="bg-white rounded-lg border shadow-sm p-6">
              <p className="text-base text-muted-foreground leading-relaxed">
                Claim text is anonymized before logging. No personal information
                is captured.
              </p>
            </div>
            <div className="bg-white rounded-lg border shadow-sm p-6">
              <p className="text-base text-muted-foreground leading-relaxed">
                All verification records auto-delete after 24 hours.
              </p>
            </div>
            <div className="bg-white rounded-lg border shadow-sm p-6">
              <p className="text-base text-muted-foreground leading-relaxed">
                No accounts, no tracking, no cookies beyond what's technically
                necessary.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Limitations */}
      <section className="py-16 bg-muted/30">
        <div className="container max-w-3xl mx-auto px-4">
          <div className="text-center mb-8">
            <div className="h-12 w-12 rounded-lg bg-[#1C7393] flex items-center justify-center mx-auto mb-4">
              <AlertTriangle className="h-6 w-6 text-white" />
            </div>
            <h2 className="text-3xl font-bold">Known Limitations</h2>
          </div>
          <div className="space-y-3 max-w-2xl mx-auto">
            <div className="bg-white rounded-lg border shadow-sm p-5">
              <p className="text-base text-muted-foreground leading-relaxed">
                <strong className="text-foreground">Official sources only</strong> — Compares against Electoral Commission
                announcements, not media or observer reports.
              </p>
            </div>
            <div className="bg-white rounded-lg border shadow-sm p-5">
              <p className="text-base text-muted-foreground leading-relaxed">
                <strong className="text-foreground">Entity extraction accuracy</strong> — ~85% for clear text,
                ~70% for images. Low-quality screenshots may not parse well.
              </p>
            </div>
            <div className="bg-white rounded-lg border shadow-sm p-5">
              <p className="text-base text-muted-foreground leading-relaxed">
                <strong className="text-foreground">English only</strong> — No local language
                support yet.
              </p>
            </div>
            <div className="bg-white rounded-lg border shadow-sm p-5">
              <p className="text-base text-muted-foreground leading-relaxed">
                <strong className="text-foreground">Not real-time</strong> — Updates when we scrape EC data,
                which may lag behind live announcements.
              </p>
            </div>
            <div className="bg-white rounded-lg border shadow-sm p-5">
              <p className="text-base text-muted-foreground leading-relaxed">
                <strong className="text-foreground">Final results only</strong> — Cannot verify claims about
                the vote tallying process itself.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Open Source + CTA */}
      <section className="py-16">
        <div className="container max-w-3xl mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-4">Open Source</h2>
          <p className="text-lg text-muted-foreground leading-relaxed mb-2 max-w-2xl mx-auto">
            Yesveri is an open-source project under the MIT license. The scraper
            code, entity extraction logic, matching algorithm, and database
            schemas are all public. We believe transparency builds trust.
          </p>
          <p className="text-lg text-muted-foreground leading-relaxed mb-10">
            Developed by Neuravox.
          </p>
          <Button size="lg" asChild>
            <Link href="/verify">
              Try It Now
              <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </Button>
        </div>
      </section>
    </div>
  );
}
