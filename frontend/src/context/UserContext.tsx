import { createContext, useContext, useState } from "react";

/**
 * Ideally, this would correspond to the logged-in user's email, but for now it's a static email.
 */

const UserContext = createContext({
	userEmail: "mayasivannj@gmail.com",
	setUserEmail: (_email: string) => {},
});

export function useUser() {
	const context = useContext(UserContext);
	if (!context) {
		throw new Error("useUser must be used within a UserProvider");
	}
	return context;
}

export function UserProvider({ children }: { children: React.ReactNode }) {
	const [userEmail, setUserEmail] = useState<string>("");

	const value = { userEmail, setUserEmail };

	return <UserContext.Provider value={value}>{children}</UserContext.Provider>;
}
