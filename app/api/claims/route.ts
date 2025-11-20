import { NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

export async function GET() {
    try {
        // Read processed claims from backend
        const backendPath = path.join(process.cwd(), '../smart-claim/backend/data/claims.json')

        if (!fs.existsSync(backendPath)) {
            return NextResponse.json({ claims: [] })
        }

        const data = fs.readFileSync(backendPath, 'utf-8')
        const claims = JSON.parse(data)

        return NextResponse.json({ claims })
    } catch (error) {
        console.error('Error reading claims:', error)
        return NextResponse.json({ error: 'Failed to load claims' }, { status: 500 })
    }
}

export async function POST(request: Request) {
    try {
        const body = await request.json()
        const { claim } = body

        // Read current mockData
        const mockDataPath = path.join(process.cwd(), 'app/data/mockData.ts')
        let mockDataContent = fs.readFileSync(mockDataPath, 'utf-8')

        // TODO: Parse and add new claim to mockClaims array
        // This is a simplified version - you may want to use a proper TS parser

        return NextResponse.json({ success: true, message: 'Claim added' })
    } catch (error) {
        console.error('Error adding claim:', error)
        return NextResponse.json({ error: 'Failed to add claim' }, { status: 500 })
    }
}
