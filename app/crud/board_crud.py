from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models import Board
from app.schemas.board_schema import BoardCreate, BoardUpdate


def create_board(db_session: Session, board_create: BoardCreate, user_id: int) -> Board:
    # 게시판 생성
    board = Board(
        name=board_create.name, public=board_create.public, count=0, user_id=user_id
    )

    db_session.add(board)
    db_session.commit()
    db_session.refresh(board)

    return board


def update_board(db_session: Session, board: Board, board_update: BoardUpdate) -> Board:
    # 게시판 업데이트
    if board_update.name:
        board.name = board_update.name
    if board_update.public is not None:
        board.public = board_update.public

    db_session.add(board)
    db_session.commit()
    db_session.refresh(board)

    return board


def delete_board(db_session: Session, board: Board) -> None:
    # 게시판 삭제 (hard delete)
    db_session.delete(board)
    db_session.commit()


def get_board_by_id(db_session: Session, id: int) -> Board | None:
    # ID로 게시판 정보 읽기
    return db_session.get(Board, id)


def get_board_by_name(db_session: Session, name: str) -> Board | None:
    # 이름으로 게시판 정보 읽기
    statement = select(Board).filter_by(name=name)
    user = db_session.execute(statement).scalar_one_or_none()
    return user
