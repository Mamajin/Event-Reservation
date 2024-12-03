import React, { createContext, useContext, useState, useEffect } from "react";
import { USER_STATUS } from "../constants";

const ThemeContext = createContext();

export const ThemeProvider = ({ children }) => {
    const [role, setRole] = useState(null);
    const [theme, setTheme] = useState(null);

    useEffect(() => {
        const role = localStorage.getItem(USER_STATUS);

        if (role) {
            setRole(role);
            setTheme(getThemeForRole(role));
        } else {
            setRole("Attendee");
            setTheme(getThemeForRole("Attendee"));
        }
    }, []);

    const getThemeForRole = (role) => {
        switch (role) {
            case "Organizer":
                return {
                    primary: "#B0E0E6",
                    secondary: "#B8B0D1",
                    accent: "#C080BB",
                    neutral: "#C850A6",
                    base: "#D02090",
                };
            case "Attendee":
            default:
                return {
                    primary: "#B0E0E6",
                    secondary: "#5A83CD",
                    accent: "#6A5ACD",
                    neutral: "#A35ACD",
                    base: "#CD5ABD",
                };
        }
    };

    return (
        <ThemeContext.Provider value={{ role, theme }}>
            {children}
        </ThemeContext.Provider>
    );
};

export const useTheme = () => useContext(ThemeContext);
