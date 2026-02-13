import { Link } from "wouter";
import { Lock } from "lucide-react";

export function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="py-6 px-4 border-t">
      <div className="container mx-auto max-w-6xl">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div className="flex flex-col md:flex-row items-center gap-6">
            <Link href="/about" className="text-muted-foreground hover:text-foreground text-sm">
              About
            </Link>
            <Link href="/verify" className="text-muted-foreground hover:text-foreground text-sm">
              Verify Claim
            </Link>
          </div>

          <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
            <Lock className="h-3 w-3" />
            <span>Claims auto-deleted after 24 hours. No images stored.</span>
          </div>

          <p className="text-sm text-muted-foreground">
            &copy; {currentYear} Yesveri by Neuravox. Open-source under MIT License.
          </p>
        </div>
      </div>
    </footer>
  );
}
