import { Info, ClipboardCheck } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Link } from "wouter";
import neuravoxLogo from "@assets/logo.png";

export function Header() {
  return (
    <header className="mb-8 pt-4 px-4">
      <div className="flex items-center justify-between mb-6">
        <Link href="/" className="flex items-center space-x-2 hover:opacity-90 transition-opacity">
          <img src={neuravoxLogo} alt="Yesveri Logo" className="h-10 w-10" />
          <div className="flex flex-col">
            <h1 className="text-2xl font-bold leading-tight">Yesveri</h1>
            <span className="text-xs text-muted-foreground">Uganda Election Verification</span>
          </div>
        </Link>

        <div className="flex items-center space-x-4">
          <Button variant="ghost" asChild size="sm" className="hidden md:flex items-center">
            <Link href="/about">
              <Info className="h-4 w-4 mr-2" />
              About
            </Link>
          </Button>

          <Button variant="ghost" asChild size="sm" className="hidden md:flex items-center">
            <Link href="/verify">
              <ClipboardCheck className="h-4 w-4 mr-2" />
              Verify Claim
            </Link>
          </Button>
        </div>
      </div>

      <p className="text-muted-foreground max-w-3xl">
        Verify election claims against official Electoral Commission data. We show what we found, what the official record says, and let you judge.
      </p>
    </header>
  );
}
