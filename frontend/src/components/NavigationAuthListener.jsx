// src/components/NavigationAuthListener.jsx
import { useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const NavigationAuthListener = () => {

	const location = useLocation();
	const navigate = useNavigate();
	const { user, token, reauthToken, loading, reauthenticate } = useAuth();
	const lastPathRef = useRef(null);
	const reauthInProgressRef = useRef(false);


  // Trigger reauthentication on navigation to keep user data fresh
  useEffect(() => {
    const triggerReauthOnNavigation = async () => {
      const currentPath = location.pathname;

      // Only reauth if:
      // 1. User is already authenticated
      // 2. We're not currently loading
      // 3. We're not already doing reauthentication
      // 4. The path has actually changed
      // 5. We're not on public pages
      if (
        user &&
        token &&
        reauthToken &&
        !loading &&
        !reauthInProgressRef.current
      ) {
        const publicPaths = ["/", "/login", "/signup"];

        // Skip reauth for public pages
        if (!publicPaths.includes(currentPath)) {
          // Only reauth if the path has actually changed
          if (
            lastPathRef.current !== null &&
            lastPathRef.current !== currentPath
          ) {
            console.log(
              `Navigation detected: ${lastPathRef.current} → ${currentPath}, triggering reauthentication...`
            );
            reauthInProgressRef.current = true;


						try {
							const success = await reauthenticate();
							if (success) {
								console.log("Navigation reauth successful");
							} else {
								console.log(
									"Navigation reauth failed - user will be logged out"
								);
								navigate("/login", { replace: true });
							}
						} catch (error) {
							console.error("Navigation reauth error:", error);
						} finally {
							reauthInProgressRef.current = false;
						}
					}
				}
			}


      // Update last path reference
      lastPathRef.current = currentPath;
    };

    triggerReauthOnNavigation();
  }, [location.pathname]); // Only depend on pathname changes

  // This component doesn't render anything, it just listens for navigation changes
  return null;
};

export default NavigationAuthListener;
