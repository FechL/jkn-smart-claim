import { NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

export async function GET(
    request: Request,
    { params }: { params: Promise<{ id: string }> }
) {
    try {
        const { id: claimId } = await params

        // Read claims from JSON file
        const claimsPath = path.join(process.cwd(), 'smart-claim/backend/data/claims.json')

        if (!fs.existsSync(claimsPath)) {
            return NextResponse.json({
                error: 'Claims file not found'
            }, { status: 404 })
        }

        const data = fs.readFileSync(claimsPath, 'utf-8')
        const claims = JSON.parse(data)

        // Find the claim
        const claim = claims.find((c: any) => c.id === claimId || c.claim_id === claimId)

        if (!claim) {
            return NextResponse.json({
                error: 'Claim not found'
            }, { status: 404 })
        }

        return NextResponse.json({ claim })
    } catch (error) {
        console.error('Error reading claim:', error)
        return NextResponse.json({
            error: 'Failed to load claim'
        }, { status: 500 })
    }
}


export async function PATCH(
    request: Request,
    { params }: { params: Promise<{ id: string }> }
) {
    try {
        const body = await request.json()
        const { status } = body
        const { id: claimId } = await params

        // Read claims from JSON file (same path as GET endpoint)
        const claimsPath = path.join(process.cwd(), 'smart-claim/backend/data/claims.json')

        if (!fs.existsSync(claimsPath)) {
            return NextResponse.json({
                error: 'Claims file not found'
            }, { status: 404 })
        }

        const data = fs.readFileSync(claimsPath, 'utf-8')
        const claims = JSON.parse(data)

        // Find and update the claim
        const claimIndex = claims.findIndex((c: any) => c.id === claimId || c.claim_id === claimId)

        if (claimIndex === -1) {
            return NextResponse.json({
                error: 'Claim not found'
            }, { status: 404 })
        }

        // Update the status
        claims[claimIndex].status = status

        // Write back to file
        fs.writeFileSync(claimsPath, JSON.stringify(claims, null, 2), 'utf-8')

        return NextResponse.json({
            success: true,
            message: 'Claim status updated',
            claimId,
            status,
            claim: claims[claimIndex]
        })
    } catch (error) {
        console.error('Error updating claim status:', error)
        return NextResponse.json({
            error: 'Failed to update claim status'
        }, { status: 500 })
    }
}
