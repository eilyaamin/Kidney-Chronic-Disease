import React from "react";
import { Navbar, NavbarContent, NavbarItem, Link, Button } from "@nextui-org/react";
import { useNavigate, useLocation } from "react-router-dom";

const Navigationbar: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleButtonClick = () => {
    // Perform any necessary logic here (if needed)
    // Redirect to a specific route using navigate()
    navigate("/");
  };

  // Check if the current URL is not at the base path ("/")
  const isNotBasePath = location.pathname !== "/";

  return (
    <Navbar maxWidth="full" position="static">
      <NavbarContent justify="end">
        <NavbarItem>
          {isNotBasePath && (
            <Button
              as={Link}
              href="#"
              variant="ghost"
              onClick={handleButtonClick}
            >
              Main Page
            </Button>
          )}
        </NavbarItem>
      </NavbarContent>
    </Navbar>
  );
};

export default Navigationbar;
