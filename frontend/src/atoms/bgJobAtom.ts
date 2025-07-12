import { atom } from "jotai";

export const bgJobAtom = atom<{ jobId: string } | null>(null);
