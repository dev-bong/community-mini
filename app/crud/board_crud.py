from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import select, or_, and_

from app.models import Board
from app.schemas.board_schema import BoardCreate, BoardUpdate


def create_board(db_session: Session, board_create: BoardCreate, user_id: int) -> Board:
    """
    게시판 생성
    """
    board = Board(
        name=board_create.name, public=board_create.public, count=0, user_id=user_id
    )

    db_session.add(board)
    db_session.commit()
    db_session.refresh(board)

    return board


def update_board(db_session: Session, board: Board, board_update: BoardUpdate) -> Board:
    """
    게시판 업데이트
    """
    if board_update.name:
        board.name = board_update.name
    if board_update.public is not None:
        board.public = board_update.public

    db_session.add(board)
    db_session.commit()
    db_session.refresh(board)

    return board


def update_count(db_session: Session, board: Board, num: int) -> None:
    board.count += num
    db_session.add(board)
    db_session.commit()


def delete_board(db_session: Session, board: Board) -> None:
    """
    게시판 삭제 (hard delete)
    """
    db_session.delete(board)
    db_session.commit()


def get_board_by_id(db_session: Session, id: int) -> Board | None:
    """
    ID로 게시판 정보 읽기
    """
    return db_session.get(Board, id)


def get_board_by_name(db_session: Session, name: str) -> Board | None:
    """
    이름으로 게시판 정보 읽기
    """
    statement = select(Board).filter_by(name=name)
    user = db_session.execute(statement).scalar_one_or_none()
    return user


def get_boards(
    db_session: Session, user_id: int | None, offset: int, limit: int
) -> List[Board] | None:
    """
    접근 가능한 게시판 목록 조회 (offset pagination, 게시판 내 게시글 많은 순서로..)
    """
    if isinstance(user_id, int):
        # 로그인 상태 O : public이거나, private면서 본인이 생성한 게시판들
        statement = select(Board).filter(
            or_(
                Board.public == True,
                and_(Board.public == False, Board.user_id == user_id),
            )
        )
    else:
        # 로그인 상태 X : public인 게시판들만 모음
        statement = select(Board).filter(Board.public == True)

    statement = statement.order_by(Board.count.desc())  # 게시글 개수 기준으로 정렬
    statement = statement.offset(offset).limit(limit)  # offset 페이징 적용

    boards = db_session.execute(statement).scalars().all()
    return boards
