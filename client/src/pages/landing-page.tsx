import { Link } from "wouter";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
  Shield,
  ImageIcon,
  Zap,
  Lock,
  CheckCircle,
  XCircle,
  AlertTriangle,
  ArrowRight,
} from "lucide-react";

export default function LandingPage() {
  return (
    <div className="container max-w-6xl px-4">
      {/* Hero */}
      <section className="py-16 md:py-24 text-center">
        <h1 className="text-4xl md:text-5xl font-bold mb-6 leading-tight">
          Verify Election Claims
          <br />
          <span className="text-primary">Against Official EC Data</span>
        </h1>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto mb-8">
          Compare claims about Uganda election results to official Electoral
          Commission announcements. We don't decide truth — we show alignment
          and let you judge.
        </p>
        <div className="flex justify-center gap-4">
          <Button size="lg" asChild>
            <Link href="/verify">
              Verify a Claim
              <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </Button>
          <Button variant="outline" size="lg" asChild>
            <Link href="/about">Learn More</Link>
          </Button>
        </div>
      </section>

      {/* Alignment States Preview */}
      <section className="py-12">
        <h2 className="text-2xl font-bold text-center mb-8">
          What You'll See
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-3xl mx-auto">
          <div className="flex items-center gap-3 p-4 rounded-lg bg-green-50 border border-green-200">
            <CheckCircle className="h-6 w-6 text-green-700 flex-shrink-0" />
            <div>
              <p className="font-medium text-green-800">Matches</p>
              <p className="text-xs text-green-700">Aligns with EC data</p>
            </div>
          </div>
          <div className="flex items-center gap-3 p-4 rounded-lg bg-red-50 border border-red-200">
            <XCircle className="h-6 w-6 text-red-700 flex-shrink-0" />
            <div>
              <p className="font-medium text-red-800">Conflicts</p>
              <p className="text-xs text-red-700">Contradicts EC data</p>
            </div>
          </div>
          <div className="flex items-center gap-3 p-4 rounded-lg bg-yellow-50 border border-yellow-200">
            <AlertTriangle className="h-6 w-6 text-yellow-700 flex-shrink-0" />
            <div>
              <p className="font-medium text-yellow-800">No Data</p>
              <p className="text-xs text-yellow-700">EC hasn't announced yet</p>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-16">
        <h2 className="text-2xl font-bold text-center mb-10">
          Built for Uganda's Information Reality
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card>
            <CardContent className="pt-6 text-center">
              <Shield className="h-10 w-10 mx-auto mb-4 text-primary" />
              <h3 className="font-semibold mb-2">Official Sources</h3>
              <p className="text-sm text-muted-foreground">
                Every data point comes from the Electoral Commission with URL,
                timestamp, and content hash.
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6 text-center">
              <ImageIcon className="h-10 w-10 mx-auto mb-4 text-primary" />
              <h3 className="font-semibold mb-2">Image Verification</h3>
              <p className="text-sm text-muted-foreground">
                Upload WhatsApp screenshots or social media posts. We extract
                the text and check it.
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6 text-center">
              <Zap className="h-10 w-10 mx-auto mb-4 text-primary" />
              <h3 className="font-semibold mb-2">Instant Results</h3>
              <p className="text-sm text-muted-foreground">
                Optimized for low bandwidth. Page loads under 100KB, results in
                under 3 seconds.
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6 text-center">
              <Lock className="h-10 w-10 mx-auto mb-4 text-primary" />
              <h3 className="font-semibold mb-2">Privacy First</h3>
              <p className="text-sm text-muted-foreground">
                No image storage. Claims anonymized. Auto-delete after 24 hours.
                No personal data collected.
              </p>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-16">
        <h2 className="text-2xl font-bold text-center mb-10">How It Works</h2>
        <div className="max-w-2xl mx-auto space-y-6">
          <div className="flex gap-4 items-start">
            <div className="flex-shrink-0 h-8 w-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center font-bold text-sm">
              1
            </div>
            <div>
              <h3 className="font-semibold mb-1">Submit a claim</h3>
              <p className="text-sm text-muted-foreground">
                Paste text or upload a screenshot of an election claim from
                WhatsApp, Twitter, Facebook, or any source.
              </p>
            </div>
          </div>
          <div className="flex gap-4 items-start">
            <div className="flex-shrink-0 h-8 w-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center font-bold text-sm">
              2
            </div>
            <div>
              <h3 className="font-semibold mb-1">We extract the details</h3>
              <p className="text-sm text-muted-foreground">
                Our system identifies candidate names, vote counts, districts,
                and percentages from the claim text.
              </p>
            </div>
          </div>
          <div className="flex gap-4 items-start">
            <div className="flex-shrink-0 h-8 w-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center font-bold text-sm">
              3
            </div>
            <div>
              <h3 className="font-semibold mb-1">Compare against official data</h3>
              <p className="text-sm text-muted-foreground">
                Extracted details are matched against stored Electoral Commission
                announcements with source references.
              </p>
            </div>
          </div>
          <div className="flex gap-4 items-start">
            <div className="flex-shrink-0 h-8 w-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center font-bold text-sm">
              4
            </div>
            <div>
              <h3 className="font-semibold mb-1">See the result</h3>
              <p className="text-sm text-muted-foreground">
                View the alignment status, a side-by-side comparison, and the
                official source reference. You judge.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-16 text-center">
        <div className="bg-gradient-to-r from-primary/10 to-primary/5 p-10 rounded-lg">
          <h2 className="text-2xl font-bold mb-4">
            Got a claim to check?
          </h2>
          <p className="text-muted-foreground mb-6 max-w-lg mx-auto">
            Verify election claims in seconds. No account needed, no data
            stored.
          </p>
          <Button size="lg" asChild>
            <Link href="/verify">
              Start Verifying
              <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </Button>
        </div>
      </section>
    </div>
  );
}
