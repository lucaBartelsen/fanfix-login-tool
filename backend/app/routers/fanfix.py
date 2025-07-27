from fastapi import APIRouter, Depends, HTTPException
from playwright.async_api import async_playwright
from app.dependencies import get_current_active_user
from app.models.user import User
from pydantic import BaseModel

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
async def login_to_fanfix(
    login_data: LoginRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Use Playwright to login to FanFix and return session cookies
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            # Navigate to login page
            await page.goto('https://auth.fanfix.io/login')
            
            # Fill in credentials
            await page.fill('input[type="email"]', login_data.username)
            await page.fill('input[type="password"]', login_data.password)
            
            # Click login button
            await page.click('button[type="submit"]')
            
            # Wait for navigation or login completion
            await page.wait_for_url('https://fanfix.io/*', timeout=10000)
            
            # Get cookies
            cookies = await context.cookies()
            
            await browser.close()
            
            return {
                "success": True,
                "cookies": cookies
            }
            
        except Exception as e:
            await browser.close()
            raise HTTPException(status_code=400, detail=f"Login failed: {str(e)}")