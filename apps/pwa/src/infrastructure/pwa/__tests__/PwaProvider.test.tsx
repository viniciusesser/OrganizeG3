import {
    act,
    fireEvent,
    render,
    screen,
} from "@testing-library/react";
import {
    beforeEach,
    describe,
    expect,
    it,
    vi,
} from "vitest";

import {
    PwaProvider,
} from "@/infrastructure/pwa/PwaProvider";
import {
    usePwa,
} from "@/infrastructure/pwa/usePwa";

const {
    registerSWMock,
} = vi.hoisted(() => ({
    registerSWMock: vi.fn(() =>
        vi.fn(async () => undefined),
    ),
}));

vi.mock("virtual:pwa-register", () => ({
    registerSW: registerSWMock,
}));

function PwaConsumer() {
    const {
        canInstall,
        installApp,
        isInstalled,
        isOnline,
    } = usePwa();

    return (
        <div>
            <span>{isOnline ? "online" : "offline"}</span>
            <span>
                {isInstalled ? "instalado" : "não instalado"}
            </span>
            {canInstall ? (
                <button
                    onClick={() => {
                        void installApp();
                    }}
                    type="button"
                >
                    instalar
                </button>
            ) : null}
        </div>
    );
}

describe("PwaProvider", () => {
    beforeEach(() => {
        registerSWMock.mockClear();
        vi.stubGlobal(
            "matchMedia",
            vi.fn(() => ({
                addEventListener: vi.fn(),
                dispatchEvent: vi.fn(),
                matches: false,
                media: "(display-mode: standalone)",
                onchange: null,
                removeEventListener: vi.fn(),
            })),
        );
    });

    it("acompanha a conectividade do navegador", () => {
        render(
            <PwaProvider>
                <PwaConsumer />
            </PwaProvider>,
        );

        act(() => {
            window.dispatchEvent(new Event("offline"));
        });

        expect(
            screen.getByText("offline"),
        ).toBeInTheDocument();

        act(() => {
            window.dispatchEvent(new Event("online"));
        });

        expect(
            screen.getByText("online"),
        ).toBeInTheDocument();
    });

    it("oferece a instalação quando o navegador a disponibiliza", async () => {
        const prompt = vi.fn(async () => undefined);
        const installEvent = new Event(
            "beforeinstallprompt",
            { cancelable: true },
        );

        Object.assign(installEvent, {
            prompt,
            userChoice: Promise.resolve({
                outcome: "accepted",
                platform: "web",
            }),
        });

        render(
            <PwaProvider>
                <PwaConsumer />
            </PwaProvider>,
        );

        act(() => {
            window.dispatchEvent(installEvent);
        });

        fireEvent.click(
            screen.getByRole("button", {
                name: "instalar",
            }),
        );

        await screen.findByText("instalado");

        expect(prompt).toHaveBeenCalledOnce();
    });
});