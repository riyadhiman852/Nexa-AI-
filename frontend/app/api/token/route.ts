import { NextResponse } from 'next/server';
import {
  AccessToken,
  type AccessTokenOptions,
  type VideoGrant,
} from 'livekit-server-sdk';
import { RoomConfiguration } from '@livekit/protocol';

type ConnectionDetails = {
  serverUrl: string;
  roomName: string;
  participantName: string;
  participantToken: string;
};

// NOTE: you are expected to define the following environment variables in `.env.local`:
const API_KEY = process.env.LIVEKIT_API_KEY;
const API_SECRET = process.env.LIVEKIT_API_SECRET;
const LIVEKIT_URL = process.env.LIVEKIT_URL;
const AGENT_NAME = process.env.AGENT_NAME;

// Don't cache the results
export const revalidate = 0;

export async function POST(req: Request) {
  try {
    if (LIVEKIT_URL === undefined) {
      throw new Error('LIVEKIT_URL is not defined');
    }

    if (API_KEY === undefined) {
      throw new Error('LIVEKIT_API_KEY is not defined');
    }

    if (API_SECRET === undefined) {
      throw new Error('LIVEKIT_API_SECRET is not defined');
    }

    // Parse room config from request body (if provided).
    const body = await req.json().catch(() => ({}));

    let roomConfig: RoomConfiguration | undefined;

    if (body?.room_config) {
      roomConfig = RoomConfiguration.fromJson(body.room_config, {
        ignoreUnknownFields: true,
      });
    } else if (AGENT_NAME) {
      // When AGENT_NAME is set, configure explicit agent dispatch
      // so the named agent worker picks up the job.
      roomConfig = RoomConfiguration.fromJson(
        { agents: [{ agentName: AGENT_NAME }] },
        { ignoreUnknownFields: true }
      );
    }

    // Generate participant identity.
    // The first visit gets a new ID.
    // Future calls from the same browser reuse the same ID.
    const participantName = 'user';

    const cookieHeader = req.headers.get('cookie') ?? '';

    const existingUserId = cookieHeader
      .split(';')
      .map((cookie) => cookie.trim())
      .find((cookie) => cookie.startsWith('nexa_user_id='))
      ?.split('=')[1];

    const userId = existingUserId || crypto.randomUUID();

    const participantIdentity = `nexa_user_${userId}`;

    // Each call still gets its own LiveKit room.
    const roomName = `voice_assistant_room_${Math.floor(
      Math.random() * 10_000
    )}`;

    const participantToken = await createParticipantToken(
      {
        identity: participantIdentity,
        name: participantName,
      },
      roomName,
      roomConfig
    );

    // Return connection details.
    const data: ConnectionDetails = {
      serverUrl: LIVEKIT_URL,
      roomName,
      participantName,
      participantToken,
    };

    const headers = new Headers({
      'Cache-Control': 'no-store',
    });

    const response = NextResponse.json(data, { headers });

    // Save the user ID in a cookie the first time.
    if (!existingUserId) {
      response.cookies.set('nexa_user_id', userId, {
        httpOnly: true,
        sameSite: 'lax',
        secure: process.env.NODE_ENV === 'production',
        maxAge: 60 * 60 * 24 * 365,
        path: '/',
      });
    }

    return response;
  } catch (error) {
    if (error instanceof Error) {
      console.error(error);
      return new NextResponse(error.message, { status: 500 });
    }

    return new NextResponse('Unknown error', { status: 500 });
  }
}

function createParticipantToken(
  userInfo: AccessTokenOptions,
  roomName: string,
  roomConfig?: RoomConfiguration
): Promise<string> {
  const at = new AccessToken(API_KEY, API_SECRET, {
    ...userInfo,
    ttl: '15m',
  });

  const grant: VideoGrant = {
    room: roomName,
    roomJoin: true,
    canPublish: true,
    canPublishData: true,
    canSubscribe: true,
  };

  at.addGrant(grant);

  if (roomConfig) {
    at.roomConfig = roomConfig;
  }

  return at.toJwt();
}