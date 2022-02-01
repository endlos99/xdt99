// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xga99.psi.impl;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiElementVisitor;
import com.intellij.psi.util.PsiTreeUtil;
import static net.endlos.xdt99.xga99.psi.Xga99Types.*;
import com.intellij.extapi.psi.ASTWrapperPsiElement;
import net.endlos.xdt99.xga99.psi.*;

public class Xga99InstructionImpl extends ASTWrapperPsiElement implements Xga99Instruction {

  public Xga99InstructionImpl(@NotNull ASTNode node) {
    super(node);
  }

  public void accept(@NotNull Xga99Visitor visitor) {
    visitor.visitInstruction(this);
  }

  @Override
  public void accept(@NotNull PsiElementVisitor visitor) {
    if (visitor instanceof Xga99Visitor) accept((Xga99Visitor)visitor);
    else super.accept(visitor);
  }

  @Override
  @Nullable
  public Xga99ArgsFI getArgsFI() {
    return findChildByClass(Xga99ArgsFI.class);
  }

  @Override
  @Nullable
  public Xga99ArgsFII getArgsFII() {
    return findChildByClass(Xga99ArgsFII.class);
  }

  @Override
  @Nullable
  public Xga99ArgsFIII getArgsFIII() {
    return findChildByClass(Xga99ArgsFIII.class);
  }

  @Override
  @Nullable
  public Xga99ArgsFIV getArgsFIV() {
    return findChildByClass(Xga99ArgsFIV.class);
  }

  @Override
  @Nullable
  public Xga99ArgsFIX getArgsFIX() {
    return findChildByClass(Xga99ArgsFIX.class);
  }

  @Override
  @Nullable
  public Xga99ArgsFV getArgsFV() {
    return findChildByClass(Xga99ArgsFV.class);
  }

  @Override
  @Nullable
  public Xga99ArgsFX getArgsFX() {
    return findChildByClass(Xga99ArgsFX.class);
  }

  @Override
  @Nullable
  public Xga99ArgsI getArgsI() {
    return findChildByClass(Xga99ArgsI.class);
  }

  @Override
  @Nullable
  public Xga99ArgsII getArgsII() {
    return findChildByClass(Xga99ArgsII.class);
  }

  @Override
  @Nullable
  public Xga99ArgsIII getArgsIII() {
    return findChildByClass(Xga99ArgsIII.class);
  }

  @Override
  @Nullable
  public Xga99ArgsIX getArgsIX() {
    return findChildByClass(Xga99ArgsIX.class);
  }

  @Override
  @Nullable
  public Xga99ArgsVI getArgsVI() {
    return findChildByClass(Xga99ArgsVI.class);
  }

  @Override
  @Nullable
  public Xga99ArgsVII getArgsVII() {
    return findChildByClass(Xga99ArgsVII.class);
  }

  @Override
  @Nullable
  public Xga99ArgsVIII getArgsVIII() {
    return findChildByClass(Xga99ArgsVIII.class);
  }

}
