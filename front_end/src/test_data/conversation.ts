import { type Message, Role } from "../app/interfaces";

export const CONVO_1: Message[] = [
    {
        role: Role.system,
        content: "You are an intelligent assistant."
    },
    {
        role: Role.user,
        content: "Good morning, how are you"
    },
    {
        role: Role.assistant,
        content: "I am doing well. How may I help you today"
    },
    {
        role: Role.user,
        content: 'What is the meaning of the word "bamboozle"?'
    },
]

export const CONVO_2: Message[] = [
    {
        role: Role.assistant,
        content: "I am doing well. How may I help you today"
    },
    {
        role: Role.user,
        content: 'How do i use the library `pandas`'
    },
]

export const CONVO_3: Message[] = [
    {
        role: Role.assistant,
        content: "I am doing well. How may I help you today"
    },
    {
        role: Role.user,
        content: 'How do i use the library ""pandas""'
    },
]

export const CONVO_4: Message[] = [
    {
        role: Role.assistant,
        content: "I am doing well, How may I help you today"
    },
    {
        role: Role.user,
        content: 'How do i, a person, use the library \npandas\n'
    },
]
