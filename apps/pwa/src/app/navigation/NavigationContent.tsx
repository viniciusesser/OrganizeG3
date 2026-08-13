import {
    useContext,
} from "react";
import {
    NavLink,
} from "react-router";

import {
    filterNavigationGroups,
    navigationGroups,
} from "@/app/navigation/navigation";
import {
    AuthContext,
} from "@/features/auth/session/AuthContext";

export interface NavigationContentProps {
    readonly onNavigate?: () => void;
}

const EMPTY_PERMISSIONS =
    new Set<string>();

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
    const auth =
        useContext(
            AuthContext,
        );

    const visibleGroups =
        auth === null
            ? navigationGroups
            : filterNavigationGroups(
                navigationGroups,
                auth.status ===
                    "authenticated"
                    ? (
                        auth.identity
                            ?.permissions ??
                        EMPTY_PERMISSIONS
                    )
                    : EMPTY_PERMISSIONS,
            );

    return (
        <>
            {visibleGroups.map(
                (group) => {
                    const groupLabelId =
                        `og3-navigation-group-${group.id}`;

                    return (
                        <section
                            aria-labelledby={
                                groupLabelId
                            }
                            className="og3-navigation__group"
                            key={group.id}
                        >
                            <div
                                className="og3-navigation__group-label"
                                id={groupLabelId}
                            >
                                {group.label}
                            </div>

                            <ul
                                className="og3-navigation__list"
                            >
                                {group.items.map(
                                    (item) => (
                                        <li
                                            key={
                                                item.id
                                            }
                                        >
                                            <NavLink
                                                className={
                                                    getNavigationLinkClassName
                                                }
                                                end={
                                                    item.end
                                                }
                                                onClick={
                                                    onNavigate
                                                }
                                                to={
                                                    item.path
                                                }
                                            >
                                                {
                                                    item.label
                                                }
                                            </NavLink>
                                        </li>
                                    ),
                                )}
                            </ul>
                        </section>
                    );
                },
            )}
        </>
    );
}