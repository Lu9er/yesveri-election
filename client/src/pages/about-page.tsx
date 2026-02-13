import { Link } from "wouter";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
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
    <div className="container max-w-4xl px-4 py-8">
      <h1 className="text-3xl font-bold mb-2">About Yesveri</h1>
      <p className="text-muted-foreground mb-8 text-lg">
        Election claim verification for Uganda
      </p>

      {/* Mission */}
      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Our Mission</h2>
        <p className="text-muted-foreground leading-relaxed mb-4">
          Yesveri helps Ugandans verify election claims against official sources
          during a period when AI-generated misinformation is cheap and trust is
          fragile. We don't decide truth — we make official records accessible
          and show how claims align with what the Electoral Commission actually
          announced.
        </p>
        <p className="text-muted-foreground leading-relaxed">
          Our goal is to make disagreement visible: show what a claim says, what
          the official record says, and let people draw their own conclusions.
        </p>
      </section>

      {/* How It Works */}
      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-6">How It Works</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-base flex items-center gap-2">
                <Database className="h-4 w-4 text-primary" />
                1. EC Data Collection
              </CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground">
              We collect and store official Electoral Commission results with
              source URLs and retrieval timestamps. Every data point is
              traceable to its official origin.
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-base flex items-center gap-2">
                <Eye className="h-4 w-4 text-primary" />
                2. Entity Extraction
              </CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground">
              When you submit a claim (text or image), we extract candidate
              names, vote counts, percentages, and constituencies using NLP
              and OCR.
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-base flex items-center gap-2">
                <Shield className="h-4 w-4 text-primary" />
                3. Deterministic Matching
              </CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground">
              Extracted fields are compared against official records using
              deterministic rules — no AI scoring or confidence percentages.
              A number either matches or it doesn't.
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-base flex items-center gap-2">
                <Eye className="h-4 w-4 text-primary" />
                4. Transparent Results
              </CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground">
              Results show what we extracted, what the official record says,
              which fields match, and which differ. You decide what it means.
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Privacy */}
      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4 flex items-center gap-2">
          <Lock className="h-5 w-5" />
          Privacy
        </h2>
        <ul className="space-y-2 text-muted-foreground">
          <li className="flex items-start gap-2">
            <span className="text-primary mt-1">&#8226;</span>
            Uploaded images are processed for text extraction and immediately
            discarded — never stored.
          </li>
          <li className="flex items-start gap-2">
            <span className="text-primary mt-1">&#8226;</span>
            Claim text is anonymized before logging. No personal information
            is captured.
          </li>
          <li className="flex items-start gap-2">
            <span className="text-primary mt-1">&#8226;</span>
            All verification records auto-delete after 24 hours.
          </li>
          <li className="flex items-start gap-2">
            <span className="text-primary mt-1">&#8226;</span>
            No accounts, no tracking, no cookies beyond what's technically
            necessary.
          </li>
        </ul>
      </section>

      {/* Limitations */}
      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4 flex items-center gap-2">
          <AlertTriangle className="h-5 w-5" />
          Known Limitations
        </h2>
        <ul className="space-y-2 text-muted-foreground">
          <li className="flex items-start gap-2">
            <span className="text-primary mt-1">&#8226;</span>
            <strong>Uganda only</strong> — Only tracks Uganda Electoral
            Commission data.
          </li>
          <li className="flex items-start gap-2">
            <span className="text-primary mt-1">&#8226;</span>
            <strong>Official sources only</strong> — Compares against EC
            announcements, not media or observer reports.
          </li>
          <li className="flex items-start gap-2">
            <span className="text-primary mt-1">&#8226;</span>
            <strong>Entity extraction accuracy</strong> — ~85% for clear text,
            ~70% for images. Low-quality screenshots may not parse well.
          </li>
          <li className="flex items-start gap-2">
            <span className="text-primary mt-1">&#8226;</span>
            <strong>English only</strong> — No Luganda or other local language
            support yet.
          </li>
          <li className="flex items-start gap-2">
            <span className="text-primary mt-1">&#8226;</span>
            <strong>Not real-time</strong> — Updates when we scrape EC data,
            which may lag behind live announcements.
          </li>
          <li className="flex items-start gap-2">
            <span className="text-primary mt-1">&#8226;</span>
            <strong>Final results only</strong> — Cannot verify claims about
            the vote tallying process itself.
          </li>
        </ul>
      </section>

      {/* Open Source */}
      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Open Source</h2>
        <p className="text-muted-foreground leading-relaxed mb-4">
          Yesveri is an open-source project under the MIT license. The scraper
          code, entity extraction logic, matching algorithm, and database
          schemas are all public. We believe transparency builds trust.
        </p>
        <p className="text-muted-foreground leading-relaxed">
          Yesveri is developed by Neuravox.
        </p>
      </section>

      {/* CTA */}
      <div className="text-center py-8">
        <Button size="lg" asChild>
          <Link href="/verify">
            Try It Now
            <ArrowRight className="ml-2 h-4 w-4" />
          </Link>
        </Button>
      </div>
    </div>
  );
}
