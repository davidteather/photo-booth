import { writable } from "svelte/store";

export const sessionPhotoIDs = writable<string[]>([]);

export const componentIndex = writable<number>(0);
