from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import subprocess

@csrf_exempt  # ← Disable CSRF for testing (re-enable later!)
def run_code(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            code = data.get('code', '')
            
            # Save and execute code
            with open('temp.py', 'w') as f:
                f.write(code)
            result = subprocess.run(
                ['python', 'temp.py'],
                capture_output=True,
                text=True
            )
            return JsonResponse({
                'output': result.stdout,
                'error': result.stderr
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)
