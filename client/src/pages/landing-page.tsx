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
    <div>
      {/* Hero */}
      <section className="bg-[#0C2E4C] text-white py-20 md:py-28">
        <div className="container max-w-4xl mx-auto px-4 text-center">
          <p className="text-sm uppercase tracking-widest text-[#A3CCDC] mb-4">
            Official Electoral Data
          </p>
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6 leading-tight">
            Verify Election Claims{" "}
            <span className="text-[#1F9CB4]">Against Reality.</span>
          </h1>
          <p className="text-lg text-[#A3CCDC] max-w-2xl mx-auto mb-10">
            Compare election claims to official Electoral Commission
            announcements. We don't decide truth — we show alignment
            and let you judge.
          </p>
          <div className="flex justify-center gap-4">
            <Button size="lg" asChild className="bg-[#1F9CB4] hover:bg-[#1C7393] text-white">
              <Link href="/verify">
                Start Verifying
                <ArrowRight className="ml-2 h-4 w-4" />
              </Link>
            </Button>
            <Button variant="outline" size="lg" asChild className="border-[#A3CCDC] text-[#A3CCDC] hover:bg-[#A3CCDC]/10 hover:text-white">
              <Link href="/about">Learn More</Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Alignment States Preview */}
      <section className="py-16 bg-muted/30">
        <div className="container max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-2xl font-bold mb-8">What You'll See</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="flex items-center gap-3 p-5 rounded-lg bg-white border shadow-sm">
              <CheckCircle className="h-6 w-6 text-[#1C7393] flex-shrink-0" />
              <div className="text-left">
                <p className="font-semibold text-foreground">Match Found</p>
                <p className="text-xs text-muted-foreground">Aligns with official EC data</p>
              </div>
            </div>
            <div className="flex items-center gap-3 p-5 rounded-lg bg-white border shadow-sm">
              <XCircle className="h-6 w-6 text-[#0C2E4C] flex-shrink-0" />
              <div className="text-left">
                <p className="font-semibold text-foreground">Conflict Detected</p>
                <p className="text-xs text-muted-foreground">Contradicts official EC data</p>
              </div>
            </div>
            <div className="flex items-center gap-3 p-5 rounded-lg bg-white border shadow-sm">
              <AlertTriangle className="h-6 w-6 text-[#A3CCDC] flex-shrink-0" />
              <div className="text-left">
                <p className="font-semibold text-foreground">Incomplete Data</p>
                <p className="text-xs text-muted-foreground">EC hasn't announced yet</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-20">
        <div className="container max-w-5xl mx-auto px-4">
          <h2 className="text-2xl font-bold text-center mb-3">
            What Makes Yesveri Different
          </h2>
          <p className="text-muted-foreground text-center mb-12 max-w-xl mx-auto">
            From WhatsApp screenshots to low-bandwidth environments,
            every detail is designed for how people actually share information.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <Card className="border shadow-sm">
              <CardContent className="pt-6 text-center">
                <div className="h-12 w-12 rounded-lg bg-[#0C2E4C] flex items-center justify-center mx-auto mb-4">
                  <Shield className="h-6 w-6 text-white" />
                </div>
                <h3 className="font-semibold mb-2">Official Sources</h3>
                <p className="text-sm text-muted-foreground">
                  Every data point comes from the Electoral Commission with URL,
                  timestamp, and content hash.
                </p>
              </CardContent>
            </Card>
            <Card className="border shadow-sm">
              <CardContent className="pt-6 text-center">
                <div className="h-12 w-12 rounded-lg bg-[#1C7393] flex items-center justify-center mx-auto mb-4">
                  <ImageIcon className="h-6 w-6 text-white" />
                </div>
                <h3 className="font-semibold mb-2">Image OCR</h3>
                <p className="text-sm text-muted-foreground">
                  Upload WhatsApp screenshots or social media posts. We extract
                  the text and check it automatically.
                </p>
              </CardContent>
            </Card>
            <Card className="border shadow-sm">
              <CardContent className="pt-6 text-center">
                <div className="h-12 w-12 rounded-lg bg-[#1F9CB4] flex items-center justify-center mx-auto mb-4">
                  <Zap className="h-6 w-6 text-white" />
                </div>
                <h3 className="font-semibold mb-2">Instant Results</h3>
                <p className="text-sm text-muted-foreground">
                  Optimized for low bandwidth. Page loads under 100KB, results in
                  under 3 seconds on 3G.
                </p>
              </CardContent>
            </Card>
            <Card className="border shadow-sm">
              <CardContent className="pt-6 text-center">
                <div className="h-12 w-12 rounded-lg bg-[#0C2E4C] flex items-center justify-center mx-auto mb-4">
                  <Lock className="h-6 w-6 text-white" />
                </div>
                <h3 className="font-semibold mb-2">Privacy by Design</h3>
                <p className="text-sm text-muted-foreground">
                  No image storage. Claims anonymized and auto-deleted after 24
                  hours. Your data is your own.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 bg-muted/30">
        <div className="container max-w-3xl mx-auto px-4">
          <h2 className="text-2xl font-bold text-center mb-3">
            How Verification Works
          </h2>
          <p className="text-muted-foreground text-center mb-12">
            Four steps to absolute clarity.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="h-12 w-12 rounded-lg border-2 border-[#0C2E4C] flex items-center justify-center mx-auto mb-4 font-bold text-[#0C2E4C]">
                1
              </div>
              <h3 className="font-semibold mb-2">Submit Claim</h3>
              <p className="text-xs text-muted-foreground">
                Paste text or upload a screenshot from WhatsApp, Twitter, or Facebook.
              </p>
            </div>
            <div>
              <div className="h-12 w-12 rounded-lg border-2 border-[#1C7393] flex items-center justify-center mx-auto mb-4 font-bold text-[#1C7393]">
                2
              </div>
              <h3 className="font-semibold mb-2">Detail Extraction</h3>
              <p className="text-xs text-muted-foreground">
                Names, vote counts, districts, and percentages are identified automatically.
              </p>
            </div>
            <div>
              <div className="h-12 w-12 rounded-lg border-2 border-[#1F9CB4] flex items-center justify-center mx-auto mb-4 font-bold text-[#1F9CB4]">
                3
              </div>
              <h3 className="font-semibold mb-2">Cross-Reference</h3>
              <p className="text-xs text-muted-foreground">
                Details are instantly matched against stored official EC announcements.
              </p>
            </div>
            <div>
              <div className="h-12 w-12 rounded-lg border-2 border-[#0C2E4C] flex items-center justify-center mx-auto mb-4 font-bold text-[#0C2E4C]">
                4
              </div>
              <h3 className="font-semibold mb-2">Judgment</h3>
              <p className="text-xs text-muted-foreground">
                View alignment status, side-by-side comparison, and official source links.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20">
        <div className="container max-w-4xl mx-auto px-4">
          <div className="bg-[#0C2E4C] text-white p-12 md:p-16 rounded-2xl text-center">
            <h2 className="text-3xl font-bold mb-4">Got a claim to check?</h2>
            <p className="text-[#A3CCDC] mb-8 max-w-lg mx-auto">
              Verify election claims in seconds. No account needed, no personal
              data stored. Stay informed with official data.
            </p>
            <Button size="lg" asChild className="bg-white text-[#0C2E4C] hover:bg-[#A3CCDC] hover:text-[#0C2E4C]">
              <Link href="/verify">Start Verifying Now</Link>
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
}
