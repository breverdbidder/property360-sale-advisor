// middleware.ts
// Auth middleware — protects routes, refreshes sessions
import { createServerClient, type CookieOptions } from "@supabase/ssr";
import { NextResponse, type NextRequest } from "next/server";

export const runtime = "edge";

// Routes that don't require authentication
const PUBLIC_ROUTES = ["/login", "/signup", "/api/auth/callback", "/api/analyze", "/api/health"];

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Skip auth check for public routes, static assets, and API routes
  if (
    PUBLIC_ROUTES.some((r) => pathname.startsWith(r)) ||
    pathname.startsWith("/_next") ||
    pathname.startsWith("/favicon") ||
    pathname.endsWith(".ico")
  ) {
    return NextResponse.next();
  }

  let response = NextResponse.next({
    request: { headers: request.headers },
  });

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll();
        },
        setAll(cookiesToSet: { name: string; value: string; options: CookieOptions }[]) {
          cookiesToSet.forEach(({ name, value }) =>
            request.cookies.set(name, value)
          );
          response = NextResponse.next({
            request: { headers: request.headers },
          });
          cookiesToSet.forEach(({ name, value, options }) =>
            response.cookies.set(name, value, options)
          );
        },
      },
    }
  );

  // Refresh the session (important for token rotation)
  const {
    data: { user },
  } = await supabase.auth.getUser();

  // Not authenticated → redirect to login
  if (!user) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("redirect", pathname);
    return NextResponse.redirect(loginUrl);
  }

  return response;
}

export const config = {
  matcher: [
    // Match all routes except static files
    "/((?!_next/static|_next/image|favicon.ico).*)",
  ],
};
