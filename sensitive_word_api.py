"""
敏感词检测API服务
基于FastAPI的REST API封装
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import uvicorn
import os

from sensitive_word import SensitiveWordDetector


# 初始化
app = FastAPI(
    title="敏感词检测服务",
    description="基于DFA算法的敏感词检测API",
    version="1.0.0"
)

# 全局检测器实例
WORDLIST_PATH = os.path.join(os.path.dirname(__file__), 'wordlist.txt')
detector = SensitiveWordDetector(WORDLIST_PATH)


# ============ 请求/响应模型 ============

class DetectRequest(BaseModel):
    """检测请求"""
    text: str
    case_sensitive: bool = False


class DetectResponse(BaseModel):
    """检测响应"""
    has_sensitive: bool
    count: int
    words: List[str]
    positions: List[Dict]


class ReplaceRequest(BaseModel):
    """替换请求"""
    text: str
    replace_char: str = '*'
    show_count: bool = True


class ReplaceResponse(BaseModel):
    """替换响应"""
    original: str
    result: str


class BatchDetectRequest(BaseModel):
    """批量检测请求"""
    texts: List[str]


class BatchDetectResponse(BaseModel):
    """批量检测响应"""
    results: List[DetectResponse]


class ReloadResponse(BaseModel):
    """重载响应"""
    success: bool
    message: str
    stats: Dict


class StatsResponse(BaseModel):
    """统计响应"""
    total_words: int
    min_length: int
    max_length: int


# ============ API接口 ============

@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok", "service": "sensitive-word-detector"}


@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    """获取词库统计"""
    return detector.get_stats()


@app.post("/detect", response_model=DetectResponse)
async def detect_sensitive_words(request: DetectRequest):
    """
    检测文本中的敏感词
    
    - **text**: 待检测文本
    - **case_sensitive**: 是否区分大小写
    """
    if not request.text:
        return DetectResponse(
            has_sensitive=False,
            count=0,
            words=[],
            positions=[]
        )
    
    result = detector.detect(request.text, request.case_sensitive)
    
    return DetectResponse(
        has_sensitive=len(result) > 0,
        count=len(result),
        words=[w['word'] for w in result],
        positions=result
    )


@app.post("/replace", response_model=ReplaceResponse)
async def replace_sensitive_words(request: ReplaceRequest):
    """
    替换文本中的敏感词
    
    - **text**: 待处理文本
    - **replace_char**: 替换字符
    - **show_count**: 是否显示字数
    """
    if not request.text:
        return ReplaceResponse(
            original="",
            result=""
        )
    
    result = detector.replace(
        request.text,
        request.replace_char,
        request.show_count
    )
    
    return ReplaceResponse(
        original=request.text,
        result=result
    )


@app.post("/batch_detect", response_model=BatchDetectResponse)
async def batch_detect(texts: List[str]):
    """
    批量检测多个文本
    
    - **texts**: 文本列表
    """
    results = []
    for text in texts:
        result = detector.detect(text)
        results.append(DetectResponse(
            has_sensitive=len(result) > 0,
            count=len(result),
            words=[w['word'] for w in result],
            positions=result
        ))
    
    return BatchDetectResponse(results=results)


@app.post("/reload", response_model=ReloadResponse)
async def reload_wordlist():
    """
    重新加载敏感词库
    """
    global detector
    
    old_stats = detector.get_stats()
    detector = SensitiveWordDetector(WORDLIST_PATH)
    new_stats = detector.get_stats()
    
    return ReloadResponse(
        success=True,
        message=f"词库已重载",
        stats={
            "before": old_stats,
            "after": new_stats
        }
    )


@app.get("/words")
async def get_all_words():
    """获取所有敏感词"""
    return {"words": detector.get_all_words()}


@app.post("/words/add")
async def add_word(word: str):
    """添加敏感词"""
    if not word or not word.strip():
        raise HTTPException(status_code=400, detail="词不能为空")
    
    detector.add_word(word.strip())
    return {"success": True, "word": word, "stats": detector.get_stats()}


# ============ 主程序 ============

def main():
    """启动服务"""
    print("=" * 50)
    print("敏感词检测服务 v1.0.0")
    print("=" * 50)
    print(f"词库路径: {WORDLIST_PATH}")
    print(f"词库统计: {detector.get_stats()}")
    print("API文档: http://localhost:8000/docs")
    print("=" * 50)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
