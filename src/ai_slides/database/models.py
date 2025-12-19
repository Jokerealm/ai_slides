"""
SQLAlchemy database models for AI Slides
"""

import time
import hashlib
from typing import Dict, Any, List, Optional
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Project(Base):
    """Project model for storing PPT projects"""
    __tablename__ = "projects"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[str] = mapped_column(String(36), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    scenario: Mapped[str] = mapped_column(String(100), nullable=False)
    topic: Mapped[str] = mapped_column(String(255), nullable=False)
    requirements: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="draft")
    outline: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    slides_html: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    slides_data: Mapped[Optional[List[Dict[str, Any]]]] = mapped_column(JSON, nullable=True)
    confirmed_requirements: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    project_metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)  # 项目元数据，包括选择的模板ID等
    version: Mapped[int] = mapped_column(Integer, default=1)
    share_token: Mapped[Optional[str]] = mapped_column(String(64), unique=True, index=True, nullable=True)  # 分享token，用于公开访问
    share_enabled: Mapped[bool] = mapped_column(Boolean, default=False)  # 是否启用分享
    created_at: Mapped[float] = mapped_column(Float, default=time.time)
    updated_at: Mapped[float] = mapped_column(Float, default=time.time, onupdate=time.time)
    
    # Relationships
    todo_board: Mapped[Optional["TodoBoard"]] = relationship("TodoBoard", back_populates="project", uselist=False)
    versions: Mapped[List["ProjectVersion"]] = relationship("ProjectVersion", back_populates="project")
    slides: Mapped[List["SlideData"]] = relationship("SlideData", back_populates="project")


class TodoBoard(Base):
    """TODO Board model for project workflow management"""
    __tablename__ = "todo_boards"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.project_id"), unique=True)
    current_stage_index: Mapped[int] = mapped_column(Integer, default=0)
    overall_progress: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[float] = mapped_column(Float, default=time.time)
    updated_at: Mapped[float] = mapped_column(Float, default=time.time, onupdate=time.time)
    
    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="todo_board")
    stages: Mapped[List["TodoStage"]] = relationship("TodoStage", back_populates="todo_board", order_by="TodoStage.stage_index")


class TodoStage(Base):
    """TODO Stage model for individual workflow stages"""
    __tablename__ = "todo_stages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    todo_board_id: Mapped[int] = mapped_column(Integer, ForeignKey("todo_boards.id"))
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.project_id"), index=True)  # Added for direct project reference
    stage_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)  # Added index for better performance
    stage_index: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending", index=True)  # Added index for status queries
    progress: Mapped[float] = mapped_column(Float, default=0.0)
    result: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[float] = mapped_column(Float, default=time.time)
    updated_at: Mapped[float] = mapped_column(Float, default=time.time, onupdate=time.time)

    # Relationships
    todo_board: Mapped["TodoBoard"] = relationship("TodoBoard", back_populates="stages")
    project: Mapped["Project"] = relationship("Project", foreign_keys=[project_id])  # Direct project relationship


class ProjectVersion(Base):
    """Project version model for version control"""
    __tablename__ = "project_versions"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.project_id"))
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    timestamp: Mapped[float] = mapped_column(Float, default=time.time)
    data: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    
    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="versions")


class SlideData(Base):
    """Slide data model for individual PPT slides"""
    __tablename__ = "slide_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.project_id"))
    slide_index: Mapped[int] = mapped_column(Integer, nullable=False)
    slide_id: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(50), nullable=False)
    html_content: Mapped[str] = mapped_column(Text, nullable=False)
    slide_metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    template_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("ppt_templates.id"), nullable=True)
    is_user_edited: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[float] = mapped_column(Float, default=time.time)
    updated_at: Mapped[float] = mapped_column(Float, default=time.time, onupdate=time.time)

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="slides")
    template: Mapped[Optional["PPTTemplate"]] = relationship("PPTTemplate", back_populates="slides")


class PPTTemplate(Base):
    """PPT Template model for storing master templates"""
    __tablename__ = "ppt_templates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.project_id"))
    template_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # title, content, chart, image, summary
    template_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    html_template: Mapped[str] = mapped_column(Text, nullable=False)
    applicable_scenarios: Mapped[List[str]] = mapped_column(JSON, nullable=True)  # 适用场景
    style_config: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)  # 样式配置
    usage_count: Mapped[int] = mapped_column(Integer, default=0)  # 使用次数统计
    created_at: Mapped[float] = mapped_column(Float, default=time.time)
    updated_at: Mapped[float] = mapped_column(Float, default=time.time, onupdate=time.time)

    # Relationships
    project: Mapped["Project"] = relationship("Project", foreign_keys=[project_id])
    slides: Mapped[List["SlideData"]] = relationship("SlideData", back_populates="template")


class GlobalMasterTemplate(Base):
    """Global Master Template model for storing reusable master templates"""
    __tablename__ = "global_master_templates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    template_name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    html_template: Mapped[str] = mapped_column(Text, nullable=False)
    preview_image: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Base64 encoded preview image
    style_config: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)  # 样式配置
    tags: Mapped[List[str]] = mapped_column(JSON, nullable=True)  # 标签分类
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)  # 是否为默认模板
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)  # 是否启用
    usage_count: Mapped[int] = mapped_column(Integer, default=0)  # 使用次数统计
    created_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # 创建者
    created_at: Mapped[float] = mapped_column(Float, default=time.time)
    updated_at: Mapped[float] = mapped_column(Float, default=time.time, onupdate=time.time)



