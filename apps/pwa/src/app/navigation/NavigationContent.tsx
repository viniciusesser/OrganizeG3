import {
    NavLink,
} from "react-router";

import {
    navigationGroups,
} from "@/app/navigation/navigation";

export interface NavigationContentProps {
    readonly onNavigate?: () => void;
}

function getNavigationLinkClassName({
    isActive,
}: {
    readonly isActive: boolean;
}): string {
    return [
        "og3-navigation__link",
        isActive
            ? "og3-navigation__link--active"
            : undefined,
    ]
        .filter(Boolean)
        .join(" ");
}

export function NavigationContent({
    onNavigate,
}: NavigationContentProps) {
    return (
        <>
            {navigationGroups.map(
                (group) => (
                    <section
                        className="og3-navigation__group"
                        key={group.id}
                    >
                        <p
                            className="og3-navigation__group-label"
                        >
                            {group.label}
                        </p>

                        <ul
                            className="og3-navigation__list"
                        >
                            {group.items.map(
                                (item) => (
                                    <li key={item.id}>
                                        <NavLink
                                            className={
                                                getNavigationLinkClassName
                                            }
                                            end={item.end}
                                            onClick={onNavigate}
                                            to={item.path}
                                        >
                                            {item.label}
                                        </NavLink>
                                    </li>
                                ),
                            )}
                        </ul>
                    </section>
                ),
            )}
        </>
    );
}